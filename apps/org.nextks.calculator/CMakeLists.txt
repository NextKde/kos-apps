kos_add_application(kos-calculator
    APP_ID org.nextks.calculator
    URI Kos.Apps.Calculator
    DISPLAY_NAME "KOS Calculator"
    DESKTOP_FILE ${CMAKE_CURRENT_SOURCE_DIR}/data/kos-calculator.desktop.in
    ICON_FILE ${CMAKE_CURRENT_SOURCE_DIR}/data/kos-calculator.svg
    METAINFO_FILE ${PROJECT_SOURCE_DIR}/packaging/flatpak/org.nextks.calculator.metainfo.xml.in
    SOURCES
        src/main.cpp
    QML_FILES
        qml/Main.qml
        qml/CalculatorPalette.qml
        qml/CalculatorEngine.qml
        qml/HistoryStore.qml
        qml/CalculatorButton.qml
        qml/CalculatorChromeButton.qml
        qml/CalculatorGlassPanel.qml
        qml/CalculatorIcon.qml
        qml/CalculatorMenu.qml
        qml/CalculatorMenuItem.qml
        qml/CalculatorMenuSeparator.qml
        qml/CalculatorPill.qml
        qml/ConvertDisplay.qml
        qml/ConvertStore.qml
        qml/ConvertUnitChip.qml
        qml/HistoryPane.qml
        qml/Keypad.qml
        qml/UnitPicker.qml
        qml/CalculatorKeys.js
        qml/UnitTable.js
)

if(BUILD_TESTING)
    find_program(KOS_QMLTESTRUNNER NAMES qmltestrunner qmltestrunner6
        HINTS /usr/lib/qt6/bin REQUIRED)
    add_test(NAME kos-calculator.engine
        COMMAND ${KOS_QMLTESTRUNNER} -input ${CMAKE_CURRENT_SOURCE_DIR}/tests/tst_engine.qml)
    set_tests_properties(kos-calculator.engine PROPERTIES
        ENVIRONMENT "QT_QPA_PLATFORM=offscreen;QT_QUICK_BACKEND=software"
        LABELS "ui;headless" TIMEOUT 20)
endif()
