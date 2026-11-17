import QtQuick
import QtQuick.Controls
import QtTest
import "../controls" as Demo

Item {
    width: 760
    height: 500

    ApplicationWindow {
        id: host
        width: 760
        height: 500
        visible: true
        Item { id: anchor; x: host.width - 60; y: 20; width: 28; height: 28 }
        Demo.LiquidPopover {
            id: menu
            anchorItem: anchor
            Demo.LiquidPopoverItem { id: first; text: "New reminder" }
            Demo.LiquidPopoverItem { id: second; text: "Calendar settings" }
        }
    }

    TestCase {
        name: "PopoverMenuSizing"
        when: windowShown

        function checkLabels() {
            verify(menu.width > 42, "menu must not collapse to arrow geometry")
            for (let index = 0; index < menu.count; ++index) {
                const item = menu.itemAt(index)
                verify(menu.width >= item.implicitWidth + menu.leftPadding + menu.rightPadding - 1)
                for (const child of item.contentItem.children) {
                    if (child.truncated !== undefined)
                        verify(!child.truncated, "truncated menu label: " + child.text)
                }
            }
            verify(menu.x >= 0 && menu.x + menu.width <= host.width)
        }

        function test_reopenAndChangeFont_data() {
            return [
                {tag: "en", label: "Show completed reminders"},
                {tag: "zh", label: "显示已完成的提醒事项"},
                {tag: "pt", label: "Configurações do calendário"}
            ]
        }

        function test_reopenAndChangeFont(data) {
            second.text = data.label
            for (const size of [13, 12, 15, 17]) {
                first.font.pixelSize = size
                second.font.pixelSize = size
                for (let attempt = 0; attempt < 2; ++attempt) {
                    menu.openAtAnchor()
                    tryCompare(menu, "opened", true)
                    wait(20)
                    checkLabels()
                    // A checkmark changes intrinsic width after the actions
                    // have moved into Menu's internal ListView.
                    second.iconName = attempt === 0 ? "check" : ""
                    wait(20)
                    checkLabels()
                    menu.close()
                    tryCompare(menu, "visible", false)
                }
            }
        }
    }
}
