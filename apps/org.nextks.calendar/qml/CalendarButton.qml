import QtQuick
import Kos.Ui

KosButton {
    id: control
    CalendarStyle { id: design }
    implicitHeight: Math.max(design.controlHeight, contentItem.implicitHeight + topPadding + bottomPadding)
    implicitWidth: Math.max(64, contentItem.implicitWidth + leftPadding + rightPadding)
    leftPadding: 12
    rightPadding: 12
    topPadding: 4
    bottomPadding: 4
    font.pixelSize: AppTheme.fontSize(11)
    font.weight: Font.Medium
    lightLabel: true
    scale: 1
    background: Rectangle {
        radius: height / 2
        color: control.emphasized ? AppTheme.withAlpha(design.accent, control.enabled ? 1 : 0.45)
            : control.flat && !control.hovered && !control.down ? "transparent"
            : control.down ? design.selectionFill
            : control.hovered ? design.rowHoverFill : design.controlFill
    }
}
