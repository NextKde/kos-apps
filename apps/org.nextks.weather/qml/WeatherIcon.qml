import QtQuick
import Kos.Ui
import Kos.Icons as Symbols

// Weather codes are app state; all artwork comes from the platform font.
Item {
    id: root
    property int code: 0
    property bool isDay: true
    property bool pulse: false
    property real pulseOpacity: 1
    implicitWidth: 24; implicitHeight: 24
    opacity: pulseOpacity
    onPulseChanged: if (!pulse) pulseOpacity = 1
    SequentialAnimation on pulseOpacity {
        running: root.pulse && !AppTheme.reduceMotion
        loops: Animation.Infinite
        NumberAnimation { to: 0.45; duration: 550; easing.type: Easing.InOutSine }
        NumberAnimation { to: 1; duration: 550; easing.type: Easing.OutSine }
    }
    readonly property string glyph: {
        if (code === 0) return isDay ? "sun_max_fill" : "moon_fill"
        if (code === 1 || code === 2) return isDay ? "cloud_sun_fill" : "cloud_moon_fill"
        if ((code >= 51 && code <= 67) || (code >= 80 && code <= 82)) return "cloud_rain_fill"
        if ((code >= 71 && code <= 77) || code === 85 || code === 86) return "cloud_snow_fill"
        if (code >= 95) return "cloud_bolt_fill"
        return "cloud_fill"
    }
    Symbols.Icon {
        size: Math.min(root.width, root.height)
        anchors.fill: parent
        name: root.glyph
        color: root.code === 0 ? (root.isDay ? "#ffd257" : "#f7f3dc") : "#f8fbff"
    }
}
