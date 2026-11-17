import QtQuick
import Kos.Ui
import Kos.Demo as Demo

// App-local layout contract, following nextkdeAppDemo GalleryDesign 2.9.
// Compact geometry and liquid material are independent choices.
QtObject {
    readonly property color contentPlane: AppTheme.dark ? "#1C1C1E" : "#FFFFFF"
    readonly property color sidebarPlane: AppTheme.dark ? "#242426" : "#F5F5F7"
    readonly property color dialogPlane: AppTheme.dark ? "#2C2C2E" : "#F7F7F9"
    readonly property color controlFill: AppTheme.dark ? "#3A3A3C" : "#EDEDF0"
    readonly property color labelPrimary: AppTheme.text
    readonly property color labelSecondary: AppTheme.mutedText
    readonly property color liquidLabel: AppTheme.dark ? "#D6D6D6" : "#555555"
    readonly property color separator: AppTheme.dark ? "#3A3A3C" : "#E3E3E8"
    readonly property color accent: AppTheme.dark ? "#0A84FF" : "#007AFF"
    readonly property color selectionDisc: "#8E8E93"
    readonly property color selectionFill: AppTheme.dark ? "#48484C" : "#DCDCE0"
    readonly property color rowHoverFill: AppTheme.dark ? "#363639" : "#DBDBDD"
    readonly property color searchFill: controlFill
    readonly property color workspaceActive: "#e4453f"
    readonly property color segmentTrack: controlFill
    readonly property color segmentPill: AppTheme.dark ? "#636363" : "#D1D1D1"
    readonly property color positive: "#34C759"
    readonly property color warning: "#FF9F0A"
    readonly property color statusPositive: AppTheme.dark ? "#34C759" : "#24883D"
    readonly property color statusWarning: AppTheme.dark ? "#FF9F0A" : "#A85C00"
    // Shape roles stay fixed across hover, press, focus and disabled states.
    readonly property int navigationRadius: 6
    readonly property int contentRowRadius: 8
    readonly property int formGroupRadius: 14
    readonly property int menuItemRadius: 6
    readonly property int popupRadius: 12
    readonly property color formGroupFill: AppTheme.dark ? "#22FFFFFF" : "#F0F0F1"
    readonly property int sidebarWidth: AppTheme.textExtent(224)
    readonly property int rowHeight: AppTheme.textExtent(30)
    readonly property int rowInsetLeading: 8
    readonly property int rowInsetTrailing: 8
    readonly property int rowIconInset: 8
    readonly property int rowIconSize: 16
    readonly property int rowTextGap: 8
    readonly property int rowFontSize: AppTheme.fontSize(13)
    readonly property int rowDetailInset: 8
    readonly property int categoryRowHeight: AppTheme.textExtent(28)
    readonly property int categoryInset: 16
    readonly property int categoryBoxSize: 14
    readonly property int categoryBoxRadius: 3
    readonly property int categoryTextGap: 8
    readonly property int categoryFontSize: AppTheme.fontSize(13)
    readonly property int categoryHeadingTop: 12
    readonly property int categoryHeadingBottom: 4
    readonly property int miniDisc: AppTheme.textExtent(18)
    readonly property int toolbarHeight: AppTheme.textExtent(40)
    readonly property int toolbarButtonSize: AppTheme.textExtent(Demo.LiquidStyle.toolbarButtonHeight)
    readonly property int toolbarIconSize: 16
    readonly property int toolbarGap: 8
    readonly property int toolbarInsetLeft: 12
    readonly property int toolbarInsetRight: 16
    readonly property int segmentWidth: AppTheme.textExtent(224)
    readonly property int segmentHeight: AppTheme.textExtent(26)
    readonly property int dateBandHeight: AppTheme.textExtent(40)
    readonly property int dateBandInset: 16
    readonly property int dateTitleSize: AppTheme.fontSize(24)
    readonly property int dateNavHeight: AppTheme.textExtent(26)
    readonly property int dateNavTextSize: AppTheme.fontSize(11)
    readonly property int controlHeight: AppTheme.textExtent(28)
    readonly property int controlFontSize: AppTheme.fontSize(11)
    readonly property int editorInputFontSize: AppTheme.fontSize(13)
    readonly property int fieldHeight: AppTheme.textExtent(28)
    readonly property int searchHeight: AppTheme.textExtent(28)
    readonly property int searchInsetLeading: 10
    readonly property int searchInsetTrailing: 10
}
