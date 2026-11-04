#include "KosApp/ApplicationRunner.h"

#ifndef KOS_DESKTOP_ID
#define KOS_DESKTOP_ID "kos-calculator"
#endif
#ifndef KOS_ACTIVATION_ID
#define KOS_ACTIVATION_ID "org.nextkde.Kos.Calculator"
#endif

int main(int argc, char *argv[])
{
    return Kos::App::run(argc, argv, {
        QStringLiteral("kos-calculator"),
        QStringLiteral("KOS Calculator"),
        QStringLiteral(KOS_DESKTOP_ID),
        QStringLiteral(KOS_ACTIVATION_ID),
        QStringLiteral("Kos.Apps.Calculator"),
        QStringLiteral(KOS_APP_VERSION),
    });
}
