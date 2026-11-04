#include "PimStore.h"

#include <QCoreApplication>
#include <QDBusConnection>
#include <QDBusError>
#include <QDebug>
#include <QDir>
#include <QLockFile>
#include <QSocketNotifier>
#include <QTimer>

#include <cerrno>
#include <csignal>
#include <cstring>
#include <sys/socket.h>
#include <unistd.h>

namespace {

// Async-signal-safe wake-up channel: the raw handler only writes one byte,
// and the event loop does the real shutdown work so destructors still run.
int signalSocketPair[2] = {-1, -1};

void forwardSignalToEventLoop(int)
{
    const char marker = 1;
    // The sockets are non-blocking, so a burst of signals can never block
    // inside the handler.
    ::write(signalSocketPair[1], &marker, sizeof(marker));
}

bool installSignalHandlers(QCoreApplication *application)
{
    if (::socketpair(AF_UNIX, SOCK_STREAM | SOCK_NONBLOCK, 0, signalSocketPair) != 0) {
        qCritical() << "Unable to create signal socketpair:"
                    << std::strerror(errno);
        return false;
    }
    auto *notifier = new QSocketNotifier(signalSocketPair[0],
                                         QSocketNotifier::Read, application);
    QObject::connect(notifier, &QSocketNotifier::activated, application,
                     [application] {
                         char marker;
                         ::read(signalSocketPair[0], &marker, sizeof(marker));
                         // quit() unwinds exec() normally, which is what runs
                         // the store destructor and its final flush.
                         application->quit();
                     });

    struct sigaction action;
    std::memset(&action, 0, sizeof(action));
    action.sa_handler = forwardSignalToEventLoop;
    ::sigemptyset(&action.sa_mask);
    action.sa_flags = SA_RESTART;
    // QCoreApplication does not intercept SIGTERM/SIGINT on Unix; without
    // these handlers `systemctl stop` or QProcess::terminate() would kill
    // the process inside the write-debounce window and drop the last
    // acknowledged mutations.
    if (::sigaction(SIGTERM, &action, nullptr) != 0
        || ::sigaction(SIGINT, &action, nullptr) != 0) {
        qCritical() << "Unable to install termination signal handlers:"
                    << std::strerror(errno);
        return false;
    }
    return true;
}

} // namespace

int main(int argc, char *argv[])
{
    QCoreApplication application(argc, argv);
    application.setApplicationName(QStringLiteral("kos-pim-service"));
    application.setApplicationVersion(QStringLiteral(KOS_APP_VERSION));
    application.setOrganizationName(QStringLiteral("NextKde"));
    application.setOrganizationDomain(QStringLiteral("nextkde.org"));

    if (!installSignalHandlers(&application))
        return 1;

    QDBusConnection bus = QDBusConnection::sessionBus();
    if (!bus.isConnected()) {
        qCritical() << "Unable to connect to the session bus:" << bus.lastError().message();
        return 1;
    }
    // Acquire the name before even opening the store. A rejected second process
    // must not load or flush an independent in-memory copy of the same data.
    if (!bus.registerService(QStringLiteral(KOS_PIM_BUS_NAME))) {
        qCritical() << "Unable to own PIM service name:" << bus.lastError().message();
        return 1;
    }
    const QString storageDirectory = PimStore::defaultStorageDirectory();
    if (!QDir().mkpath(storageDirectory)) {
        qCritical() << "Unable to create PIM storage directory:" << storageDirectory;
        return 1;
    }
    // Also arbitrate separate session buses using the same directory. Older
    // native releases do not honor this lock; sandbox storage stays separate.
    QLockFile storageLock(QDir(storageDirectory).filePath(QStringLiteral("service.lock")));
    storageLock.setStaleLockTime(0);
    if (!storageLock.tryLock(0)) {
        qCritical() << "PIM storage is already in use or cannot be locked:" << storageDirectory
                    << storageLock.error();
        return 1;
    }
    PimStore store(storageDirectory);
    if (!bus.registerObject(QStringLiteral("/Pim"), &store,
                            QDBusConnection::ExportAllSlots
                                | QDBusConnection::ExportAllSignals)) {
        qCritical() << "Unable to export PIM object:" << bus.lastError().message();
        return 1;
    }
    // D-Bus-activated services must not outlive the session bus. This can
    // otherwise leave a detached PIM process behind when a user logs out or a
    // private test session ends.
    QTimer connectionWatchdog;
    connectionWatchdog.setInterval(1000);
    QObject::connect(&connectionWatchdog, &QTimer::timeout, &application,
                     [&application, &bus] {
                         if (!bus.isConnected())
                             application.quit();
                     });
    connectionWatchdog.start();

    return application.exec();
}
