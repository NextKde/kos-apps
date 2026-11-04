add_library(kos_pim_service_core STATIC
    src/PimStore.cpp
    src/PimStore.h
)
target_include_directories(kos_pim_service_core PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)
target_link_libraries(kos_pim_service_core PUBLIC
    Qt6::Core
    Qt6::Gui
    Qt6::DBus
    Qt6::Network
    KF6::CalendarCore
)

qt_add_executable(kos-pim-service
    src/main.cpp
)
target_link_libraries(kos-pim-service PRIVATE
    kos_pim_service_core
)
target_compile_definitions(kos-pim-service PRIVATE
    KOS_APP_VERSION="${PROJECT_VERSION}"
    KOS_PIM_BUS_NAME="${KOS_PIM_BUS_NAME}"
)
if(KOS_FLATPAK_BUILD)
    target_compile_definitions(kos_pim_service_core PRIVATE
        KOS_PIM_SANDBOX=1
        KOS_CALENDAR_DESKTOP_ID="${KOS_FLATPAK_APP_ID}"
        KOS_CALENDAR_ACTIVATION_ID="${KOS_FLATPAK_APP_ID}")
else()
    target_compile_definitions(kos_pim_service_core PRIVATE
        KOS_CALENDAR_DESKTOP_ID="kos-calendar"
        KOS_CALENDAR_ACTIVATION_ID="org.nextkde.Kos.Calendar")
endif()

set(KOS_PIM_SERVICE_EXECUTABLE "" CACHE FILEPATH
    "PIM activation executable override; empty uses this installation prefix")
if(NOT KOS_PIM_SERVICE_EXECUTABLE)
    set(KOS_PIM_SERVICE_EXECUTABLE "${CMAKE_INSTALL_FULL_BINDIR}/kos-pim-service")
endif()
option(KOS_INSTALL_PIM_ACTIVATION "Install private-prefix D-Bus activation file" ON)
option(KOS_INSTALL_PIM_SYSTEMD_UNIT "Install optional user systemd unit (installer must own it)" OFF)
if(KOS_FLATPAK_BUILD)
    if(KOS_INSTALL_PIM_SYSTEMD_UNIT)
        message(FATAL_ERROR "Flatpak uses portal autostart, not a host systemd unit")
    endif()
    set(KOS_PIM_SERVICE_EXECUTABLE "/app/bin/kos-pim-service")
endif()
set(KOS_PIM_SYSTEMD_ACTIVATION "")
if(KOS_INSTALL_PIM_SYSTEMD_UNIT)
    set(KOS_PIM_SYSTEMD_ACTIVATION "SystemdService=kos-pim-service.service")
endif()
configure_file(
    data/org.nextkde.Kos.Pim1.service.in
    ${CMAKE_CURRENT_BINARY_DIR}/${KOS_PIM_BUS_NAME}.service
    @ONLY
)
configure_file(
    data/kos-pim-service.service.in
    ${CMAKE_CURRENT_BINARY_DIR}/kos-pim-service.service
    @ONLY
)

install(TARGETS kos-pim-service
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
if(KOS_INSTALL_PIM_ACTIVATION)
    install(FILES ${CMAKE_CURRENT_BINARY_DIR}/${KOS_PIM_BUS_NAME}.service
        DESTINATION ${CMAKE_INSTALL_DATADIR}/dbus-1/services)
endif()
if(KOS_INSTALL_PIM_SYSTEMD_UNIT)
    install(FILES ${CMAKE_CURRENT_BINARY_DIR}/kos-pim-service.service
        DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/systemd/user)
endif()

if(BUILD_TESTING)
    qt_add_executable(kos-pim-store-test
        tests/PimStoreTest.cpp
    )
    target_link_libraries(kos-pim-store-test PRIVATE
        kos_pim_service_core
        Qt6::Test
    )
    add_test(NAME kos-pim.store COMMAND kos-pim-store-test)
    set_tests_properties(kos-pim.store PROPERTIES TIMEOUT 20 LABELS data)

    # dbus-run-session gates only these two D-Bus tests: a machine without it
    # still builds and runs the store test, so this probe must not be REQUIRED.
    find_program(DBUS_RUN_SESSION_EXECUTABLE dbus-run-session)
    if(DBUS_RUN_SESSION_EXECUTABLE)
        qt_add_executable(kos-pim-dbus-test
            tests/PimDbusTest.cpp
        )
        target_link_libraries(kos-pim-dbus-test PRIVATE
            Qt6::Core
            Qt6::DBus
            Qt6::Test
        )
        add_test(NAME kos-pim.dbus
            COMMAND ${DBUS_RUN_SESSION_EXECUTABLE} --
                ${CMAKE_COMMAND} -E env
                KOS_PIM_TEST_SERVICE=$<TARGET_FILE:kos-pim-service>
                $<TARGET_FILE:kos-pim-dbus-test>
        )
        set_tests_properties(kos-pim.dbus PROPERTIES TIMEOUT 20 LABELS data)

        qt_add_executable(kos-pim-client-dbus-test
            tests/PimClientDbusTest.cpp
        )
        target_link_libraries(kos-pim-client-dbus-test PRIVATE
            Kos::PimClient
            Qt6::Network
            Qt6::DBus
            Qt6::Test
        )
        add_test(NAME kos-pim.client-dbus
            COMMAND ${DBUS_RUN_SESSION_EXECUTABLE} --
                ${CMAKE_COMMAND} -E env
                KOS_PIM_TEST_SERVICE=$<TARGET_FILE:kos-pim-service>
                $<TARGET_FILE:kos-pim-client-dbus-test>
        )
        set_tests_properties(kos-pim.client-dbus PROPERTIES TIMEOUT 20 LABELS data)
    endif()
endif()
