pragma ComponentBehavior: Bound
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Kos.Ui
import Kos.Demo as Demo

KosDialog {
    id: root
    objectName: "kosSettingsDialog"
    property var settings: null
    property bool samplingAvailable: false
    readonly property bool glassEnabled: settings && samplingAvailable
        && settings.materialMode !== "solid" && !settings.reduceTransparency
    CalendarStyle { id: design }
    parent: Overlay.overlay
    anchors.centerIn: parent
    width: Math.min(550, parent ? parent.width - 32 : 550)
    height: Math.min(650, parent ? parent.height - 32 : 650)
    popupType: Popup.Item
    modal: true
    focus: true
    padding: 0
    title: qsTr("Calendar settings")
    closePolicy: Popup.CloseOnEscape
    Shortcut { sequences: [StandardKey.Preferences]; onActivated: root.open() }
    Overlay.modal: Rectangle { color: Qt.rgba(0, 0, 0, AppTheme.dark ? 0.4 : 0.16) }
    background: Rectangle {
        radius: 16
        color: design.sidebarPlane
        border.width: 1
        border.color: design.separator
    }

    component Section: Pane {
        Layout.fillWidth: true
        padding: 16
        background: Rectangle {
            radius: 12
            color: design.contentPlane
            border.width: 1
            border.color: AppTheme.withAlpha(design.separator, 0.65)
        }
    }
    component Heading: Label {
        Layout.fillWidth: true
        color: design.labelPrimary
        font.pixelSize: 14
        font.weight: Font.DemiBold
        wrapMode: Text.Wrap
    }
    component Help: Label {
        Layout.fillWidth: true
        color: design.labelSecondary
        font.pixelSize: 11
        wrapMode: Text.Wrap
    }
    component TextAction: Demo.LiquidActionButton {
        materialForm: true
        font.pixelSize: 13
        implicitHeight: Math.max(34, contentItem.implicitHeight + 16)
        cornerRadius: 8
    }
    component Choice: Demo.LiquidSegmentedControl {
        Layout.fillWidth: true
        Layout.preferredHeight: 32
        materialForm: true
        backgroundColor: design.controlFill
        selectionColor: AppTheme.dark ? "#55555B" : "#FFFFFF"
        textColor: design.labelPrimary
        mutedTextColor: design.labelSecondary
    }
    header: Item {
        implicitHeight: Math.max(72, heading.implicitHeight + 32)
        Label {
            id: heading
            x: 22; y: 16
            width: Math.max(0, closeButton.x - x - 16)
            text: root.title
            color: design.labelPrimary
            font.pixelSize: 20
            font.weight: Font.DemiBold
            wrapMode: Text.Wrap
        }
        ToolButton {
            id: closeButton
            objectName: "settingsClose"
            anchors.right: parent.right; anchors.rightMargin: 16
            anchors.verticalCenter: parent.verticalCenter
            width: 32; height: 32
            Accessible.name: qsTr("Close settings")
            contentItem: Demo.VectorIcon { name: "xmark"; size: 14; color: design.labelSecondary }
            background: Rectangle { radius: 16; color: closeButton.hovered ? design.selectionFill : design.controlFill }
            onClicked: root.close()
        }
    }
    contentItem: ScrollView {
        id: scroller
        objectName: "calendarSettingsScroll"
        clip: true
        contentWidth: availableWidth
        leftPadding: 18; rightPadding: 18
        bottomPadding: 12
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
        ColumnLayout {
            width: scroller.availableWidth
            spacing: 12
            Section {
                contentItem: ColumnLayout {
                    spacing: 10
                    Heading { text: qsTr("Color scheme") }
                    Help { text: qsTr("Use the same light or dark appearance as the calendar.") }
                    Choice {
                        objectName: "settingsAppearanceSelector"
                        labels: [qsTr("System"), qsTr("Light"), qsTr("Dark")]
                        currentIndex: root.settings ? Math.max(0, ["system", "light", "dark"].indexOf(root.settings.appearanceMode)) : 0
                        onSelectionRequested: index => { if (root.settings) root.settings.appearanceMode = ["system", "light", "dark"][index] }
                    }
                }
            }
            Section {
                contentItem: ColumnLayout {
                    spacing: 10
                    Heading { text: qsTr("Material") }
                    Help { text: qsTr("Choose how floating panels blend with the calendar.") }
                    Choice {
                        objectName: "settingsMaterialSelector"
                        labels: [qsTr("Auto"), qsTr("Glass"), qsTr("Solid")]
                        currentIndex: root.settings ? Math.max(0, ["auto", "glass", "solid"].indexOf(root.settings.materialMode)) : 0
                        onSelectionRequested: index => { if (root.settings) root.settings.materialMode = ["auto", "glass", "solid"][index] }
                    }
                    RowLayout {
                        Layout.fillWidth: true
                        Label { Layout.fillWidth: true; text: qsTr("Material opacity"); color: design.labelPrimary; font.pixelSize: 12; wrapMode: Text.Wrap }
                        Label { text: Math.round(opacitySlider.value * 100) + "%"; color: design.labelSecondary; font.pixelSize: 12 }
                    }
                    Slider {
                        id: opacitySlider
                        objectName: "settingsMaterialOpacity"
                        Layout.fillWidth: true
                        from: 0.72; to: 0.98; stepSize: 0.01
                        enabled: root.glassEnabled
                        value: root.settings ? root.settings.materialOpacity : 0.86
                        palette.highlight: design.accent
                        Accessible.name: qsTr("Material opacity")
                        onMoved: if (root.settings) root.settings.materialOpacity = value
                    }
                }
            }
            Section {
                contentItem: ColumnLayout {
                    spacing: 10
                    Heading { text: qsTr("Accessibility") }
                    Repeater {
                        model: [
                            {key: "reduceTransparency", label: qsTr("Reduce transparency"), help: qsTr("Use solid surfaces for easier reading.")},
                            {key: "reduceMotion", label: qsTr("Reduce motion"), help: qsTr("Keep transitions simple and reduce movement.")}
                        ]
                        delegate: RowLayout {
                            required property var modelData
                            Layout.fillWidth: true
                            spacing: 12
                            ColumnLayout {
                                Layout.fillWidth: true
                                Label { Layout.fillWidth: true; text: modelData.label; color: design.labelPrimary; font.pixelSize: 13; wrapMode: Text.Wrap }
                                Help { text: modelData.help }
                            }
                            Switch {
                                checked: root.settings ? root.settings[modelData.key] : false
                                Accessible.name: modelData.label
                                palette.highlight: design.accent
                                onToggled: if (root.settings) root.settings[modelData.key] = checked
                            }
                        }
                    }
                }
            }
        }
    }
    footer: Item {
        implicitHeight: Math.max(64, footerActions.implicitHeight + 24)
        Rectangle { width: parent.width; height: 1; color: design.separator }
        RowLayout {
            id: footerActions
            anchors.fill: parent
            anchors.margins: 12
            anchors.leftMargin: 18; anchors.rightMargin: 18
            spacing: 10
            TextAction {
                objectName: "settingsReset"
                text: qsTr("Restore defaults")
                onClicked: if (root.settings) { root.settings.resetAppearance() }
            }
            Item { Layout.fillWidth: true }
            TextAction { objectName: "settingsDone"; text: qsTr("Done"); highlighted: true; onClicked: root.close() }
        }
    }
}
