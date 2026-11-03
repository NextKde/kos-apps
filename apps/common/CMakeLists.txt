add_library(kos_app_core STATIC
    src/ApplicationActivation.cpp
    src/ApplicationActivation.h
    src/ApplicationPreferences.cpp
    src/ApplicationPreferences.h
    src/ApplicationQmlReloader.cpp
    include/KosApp/ApplicationQmlReloader.h
    src/ApplicationRunner.cpp
)

add_library(Kos::AppCore ALIAS kos_app_core)

target_include_directories(kos_app_core
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/../../shared/i18n>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)

find_package(Qt6 REQUIRED COMPONENTS LinguistTools)
qt_add_translations(kos_app_core
    SOURCE_TARGETS kos_app_core
    SOURCES
        ../weather/qml
        ../../shared/qml/foundation ../../shared/demo-ui
    TS_FILES translations/kos_apps_zh_CN.ts translations/kos_apps_pt_BR.ts
        translations/kos_apps_en_US.ts
    RESOURCE_PREFIX /kos/i18n
)

target_link_libraries(kos_app_core PUBLIC
    Qt6::Core
    Qt6::DBus
    Qt6::Gui
    Qt6::Qml
    Qt6::Quick
    Qt6::QuickControls2
)

if(TARGET KF6::WindowSystem)
    target_link_libraries(kos_app_core PUBLIC KF6::WindowSystem)
    target_compile_definitions(kos_app_core PRIVATE KOS_HAVE_KWINDOWSYSTEM=1)
endif()

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(kos_app_core PRIVATE
        -Wall
        -Wextra
        -Wpedantic
    )
endif()
