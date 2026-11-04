#include "KosApp/ApplicationRunner.h"

#ifndef KOS_DESKTOP_ID
#define KOS_DESKTOP_ID "kos-weather"
#define KOS_ACTIVATION_ID "org.nextkde.Weather"
#endif

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
