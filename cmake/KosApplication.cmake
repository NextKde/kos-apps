include_guard(GLOBAL)

function(kos_add_application target)
    set(oneValueArgs APP_ID URI DISPLAY_NAME DESKTOP_FILE ICON_FILE METAINFO_FILE)
    set(multiValueArgs SOURCES QML_SOURCES QML_FILES LINK_LIBRARIES)
    cmake_parse_arguments(KOS_APP "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})
    foreach(required_argument APP_ID URI DISPLAY_NAME DESKTOP_FILE METAINFO_FILE)
        if(NOT KOS_APP_${required_argument})
            message(FATAL_ERROR "kos_add_application(${target}) requires ${required_argument}")
        endif()
    endforeach()
    qt_add_executable(${target} ${KOS_APP_SOURCES})
    qt_add_qml_module(${target}
        URI ${KOS_APP_URI} VERSION 1.0 RESOURCE_PREFIX /qt/qml
        SOURCES ${KOS_APP_QML_SOURCES} QML_FILES ${KOS_APP_QML_FILES})
    target_link_libraries(${target} PRIVATE
        Kos::AppCore Kos::Ui Kos::UiPlugin Qt6::Core Qt6::Gui Qt6::Qml
        Qt6::Quick Qt6::QuickControls2 ${KOS_APP_LINK_LIBRARIES})
    target_compile_definitions(${target} PRIVATE
        KOS_APP_VERSION="${PROJECT_VERSION}"
        KOS_DESKTOP_ID="${KOS_APP_APP_ID}"
        KOS_ACTIVATION_ID="${KOS_APP_APP_ID}")
    if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
        target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic)
    endif()
    install(TARGETS ${target} RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
    set(KOS_APP_EXECUTABLE "${CMAKE_INSTALL_FULL_BINDIR}/${target}")
    if(KOS_FLATPAK_BUILD)
        set(KOS_APP_EXECUTABLE "${target}")
    endif()
    set(kos_desktop_name "${KOS_APP_APP_ID}.desktop")
    configure_file("${KOS_APP_DESKTOP_FILE}" "${CMAKE_CURRENT_BINARY_DIR}/${kos_desktop_name}" @ONLY)
    file(READ "${CMAKE_CURRENT_BINARY_DIR}/${kos_desktop_name}" kos_desktop)
    string(REPLACE "Icon=${target}" "Icon=${KOS_APP_APP_ID}" kos_desktop "${kos_desktop}")
    string(REPLACE "StartupWMClass=${target}" "StartupWMClass=${KOS_APP_APP_ID}" kos_desktop "${kos_desktop}")
    file(WRITE "${CMAKE_CURRENT_BINARY_DIR}/${kos_desktop_name}" "${kos_desktop}")
    install(FILES "${CMAKE_CURRENT_BINARY_DIR}/${kos_desktop_name}"
        DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/applications)
    if(KOS_APP_ICON_FILE)
        install(FILES "${KOS_APP_ICON_FILE}"
            DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/icons/hicolor/scalable/apps
            RENAME "${KOS_APP_APP_ID}.svg")
    endif()
    configure_file("${KOS_APP_METAINFO_FILE}"
        "${CMAKE_CURRENT_BINARY_DIR}/${KOS_APP_APP_ID}.metainfo.xml" @ONLY)
    install(FILES "${CMAKE_CURRENT_BINARY_DIR}/${KOS_APP_APP_ID}.metainfo.xml"
        DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/metainfo)
endfunction()
