    Item {
        id: reviewCapture
        anchors.fill: parent
        Component.onCompleted: Qt.callLater(function() {
            windowChrome.parent = reviewCapture
            root.Overlay.overlay.parent = reviewCapture
        })
    }
    TestCase {
        function verify(value, message) { if (!value) { console.error("TYPOGRAPHY_FAILED", message || "", new Error().stack); fail(message || "Verification failed") } }
        function compare(actual, expected, message) { if (actual !== expected) { console.error("TYPOGRAPHY_FAILED", actual, expected, message || "", new Error().stack); fail(message || "Comparison failed") } }
        function tryCompare(object, property, value, timeout) { const end = Date.now() + (timeout || 5000); while (object[property] !== value && Date.now() < end) wait(30); compare(object[property], value, property) }
        id: typographyTest
        name: "CalendarTypography"
        when: pim.ready
        windowShown: true
        property int caseCount: 0
        function visualChild(item, name) {
            if (!item) return null
            if (item.objectName === name) return item
            for (const child of item.children || []) { const found=visualChild(child,name); if (found) return found }
            return null
        }
        function allTexts(item, out) {
            if (!item || item.visible === false || item.opacity === 0) return
            if (item.text !== undefined && item.truncated !== undefined && String(item.text).length) out.push(item)
            const children = item.children || []
            for (let c of children) allTexts(c, out)
        }
        function checkLabels(item, name, strict) {
            let texts = []; allTexts(item, texts)
            let issues = []
            for (let t of texts) {
                if (t.truncated) issues.push({text:t.text, width:t.width, natural:t.implicitWidth, type:"truncated"})
                if (t.height > 0 && t.implicitHeight > t.height + 1 && t.wrapMode === Text.NoWrap)
                    issues.push({text:t.text, height:t.height, natural:t.implicitHeight, type:"height"})
            }
            console.log("TYPOGRAPHY_AUDIT", JSON.stringify({case:name,size:root.applicationSettings.textSize,issues:issues}))
            if (strict) compare(issues.length, 0, name+": "+JSON.stringify(issues))
        }
        function screenshot(name) {
            let saved=false
            verify(reviewCapture.grabToImage(result => { saved=result.saveToFile("@OUT@/"+name+".png") }), "request screenshot")
            const deadline=Date.now()+4000
            while (!saved && Date.now()<deadline) wait(40)
            verify(saved, "save screenshot")
        }
        function checkActionMenu(size, windowWidth) {
            // Opening reparents the actions into Menu's content view. Reopen and
            // change checked state to catch stale widths after that transition.
            for (let attempt = 0; attempt < 2; ++attempt) {
                mouseClick(moreButton, moreButton.width/2, moreButton.height/2)
                tryCompare(actionsMenu, "opened", true);wait(80)
                checkLabels(actionsMenu.contentItem, "actions-menu-"+size+"-"+windowWidth+"-"+attempt, true)
                verify(actionsMenu.x >= 0 && actionsMenu.x+actionsMenu.width <= root.width, "menu fits window")
                console.log("ACTION_MENU_WIDTH", size, windowWidth, attempt, actionsMenu.width)
                if (attempt === 0) {
                    if ((size === "large" || size === "extra-large") && windowWidth === 760)
                        screenshot("actions-menu-"+size+"-minimum")
                    const previous = root.showCompletedTasks
                    const toggle = actionsMenu.itemAt(1)
                    mouseClick(toggle, toggle.width/2, toggle.height/2)
                    tryCompare(root, "showCompletedTasks", !previous)
                    tryCompare(actionsMenu, "visible", false)
                } else {
                    const settingsAction = actionsMenu.itemAt(actionsMenu.count-1)
                    mouseClick(settingsAction, settingsAction.width/2, settingsAction.height/2)
                    tryCompare(settingsDialog, "opened", true)
                    tryCompare(actionsMenu, "visible", false)
                    settingsDialog.close();wait(60)
                }
            }
        }
        function test_presetsAndViews() {
            console.log("TYPOGRAPHY_STARTED")
            root.applicationSettings.reduceMotion = true
            root.applicationSettings.appearanceMode = "light"
            root.visibleMonth = new Date(2026,10,1)
            root.selectedDate = new Date(2026,10,17)
            root.now = new Date(2026,10,17,10,30)
            for (const size of ["medium", "small", "large", "extra-large"]) {
                root.width=900; root.height=630; root.sidebarExpanded=true
                settingsDialog.open(); tryCompare(settingsDialog,"opened",true)
                wait(100)
                const option=visualChild(settingsDialog.contentItem,"textSize_"+size)
                verify(option!==null)
                mouseClick(option,option.width/2,option.height/2)
                tryCompare(root.applicationSettings,"textSize",size)
                wait(120)
                compare(root.font.pixelSize, ({"small":12,"medium":13,"large":15,"extra-large":17})[size], "body font size")
                checkLabels(settingsDialog.contentItem,"settings-content",true)
                checkLabels(settingsDialog.header,"settings-header",true)
                checkLabels(settingsDialog.footer,"settings-footer",true)
                verify(findChild(settingsDialog,"settingsAccentSelector")===null)
                if (size==="extra-large" || size==="medium") screenshot("settings-"+size)
                settingsDialog.close();wait(60)
                for (const dims of [[900,630],[760,500]]) {
                    root.width=dims[0];root.height=dims[1];wait(100)
                    checkActionMenu(size, dims[0])
                    for (let view=0;view<4;view++) {
                        root.viewIndex=view;wait(90)
                        checkLabels(viewSegment,"toolbar-view-"+view+"-"+dims[0],true)
                        checkLabels(dateNavGroup,"date-navigation",true)
                        verify(dateNavGroup.y + dateNavGroup.height <= dateBand.height+1, "navigation stays in date header")
                        verify(viewSegment.x+viewSegment.width <= toolbar.width+1,"view selector fits toolbar")
                        if (!windowChrome.twoToolbarRows)
                            verify(viewSegment.x+viewSegment.width <= searchToggleButton.x,"selector avoids search")
                        if (size==="extra-large" && dims[0]===760 && view===1) screenshot("week-extra-large-minimum")
                        if (size==="extra-large" && dims[0]===760 && view===3) screenshot("year-extra-large-minimum")
                        caseCount++
                    }
                    root.sidebarExpanded=false;wait(120)
                    checkLabels(collapsedWorkspaceSwitch,"collapsed-workspace-"+dims[0],true)
                    root.sidebarExpanded=true;root.switchWorkspace(true);wait(120)
                    if (size==="extra-large" && dims[0]===760) screenshot("reminders-extra-large-minimum")
                    root.switchWorkspace(false);root.viewIndex=0
                    eventEditor.openForDate(root.selectedDate,10);eventEditor.scheduleExpanded=true;wait(120)
                    verify(eventEditor.visible)
                    verify(eventEditor.height <= root.height-15)
                    checkLabels(eventEditor.header,"event-tabs",true)
                    checkLabels(eventEditor.footer,"event-actions",true)
                    checkLabels(eventEditor.contentItem,"event-content",true)
                    if (size==="extra-large" && dims[0]===760) {
                        screenshot("event-extra-large-minimum")
                        const dateField=visualChild(eventEditor.contentItem,"eventStartDate")
                        dateField.showPicker();wait(80)
                        checkLabels(root.Overlay.overlay,"date-picker",true)
                        dateField.closePicker();wait(50)
                        const timeField=visualChild(eventEditor.contentItem,"eventStartTime")
                        timeField.showPicker();wait(80)
                        checkLabels(root.Overlay.overlay,"time-picker",true)
                        timeField.closePicker();wait(50)
                    }
                    eventEditor.close();wait(60)
                    root.openNewReminder(addButton);wait(100)
                    checkLabels(taskEditor.header,"reminder-tabs",true)
                    checkLabels(taskEditor.footer,"reminder-actions",true)
                    checkLabels(taskEditor.contentItem,"reminder-content",true)
                    verify(taskEditor.height <= root.height-15)
                    if (size==="extra-large" && dims[0]===760) screenshot("reminder-editor-extra-large-minimum")
                    taskEditor.close();wait(60)
                    caseCount++
                }
            }
            root.width=760;root.height=500
            settingsDialog.open();wait(120)
            checkLabels(settingsDialog.contentItem,"settings-minimum",true)
            checkLabels(settingsDialog.header,"settings-header-minimum",true)
            screenshot("settings-extra-large-minimum")
            settingsDialog.close()
            // A real save in the private test PIM confirms editors still work after resizing.
            eventEditor.openForDate(root.selectedDate,10)
            eventEditor.setQuickTitle("字号测试 / Long multilingual event / Reunião de planejamento")
            const eventCount=pim.events.length
            eventEditor.accept()
            const deadline=Date.now()+5000
            while (pim.events.length===eventCount && Date.now()<deadline) wait(50)
            compare(pim.events.length,eventCount+1,"save event after preset changes")
            root.width=900;root.height=630
            root.applicationSettings.appearanceMode="dark"
            settingsDialog.open();wait(150)
            screenshot("settings-extra-large-dark")
            const reset=visualChild(settingsDialog.footer,"settingsReset")
            mouseClick(reset,reset.width/2,reset.height/2)
            tryCompare(root.applicationSettings,"textSize","medium")
            compare(root.applicationSettings.appearanceMode,"system")
            console.log("CALENDAR_TYPOGRAPHY_PASSED",caseCount)
        }
    }

    Timer { interval: 1200; running: true; onTriggered: typographyTest.qtest_run() }
