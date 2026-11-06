#include "KosApp/ApplicationRunner.h"

int main(int argc, char *argv[])
{
    return Kos::App::run(argc, argv, {
        QStringLiteral("kos-weather"),
        QStringLiteral("KOS Weather"),
        QStringLiteral(KOS_DESKTOP_ID),
        QStringLiteral(KOS_ACTIVATION_ID),
        QStringLiteral("Kos.Apps.Weather"),
        QStringLiteral(KOS_APP_VERSION),
        {},
        true,
    });
}
