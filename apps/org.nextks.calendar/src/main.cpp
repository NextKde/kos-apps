#include "KosApp/ApplicationRunner.h"

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
