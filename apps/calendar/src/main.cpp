#include "KosApp/ApplicationRunner.h"

#ifndef KOS_DESKTOP_ID
#define KOS_DESKTOP_ID "kos-calendar"
#define KOS_ACTIVATION_ID "org.nextkde.Kos.Calendar"
#endif

int main(int argc, char *argv[])
{
    return Kos::App::run(argc, argv, {
        QStringLiteral("kos-calendar"),
        QStringLiteral("KOS Calendar"),
        QStringLiteral(KOS_DESKTOP_ID),
        QStringLiteral(KOS_ACTIVATION_ID),
        QStringLiteral("Kos.Apps.Calendar"),
        QStringLiteral(KOS_APP_VERSION),
        {},
        true,
    });
}
