# KOS_WEATHER_TESTS_ONLY is set by the root project when it descends here only
# for the tests below: kos-weather links Kos::Ui, which is gated behind the app
# flags, so building the application from a test-only descent would fail.
if(NOT KOS_WEATHER_TESTS_ONLY)
if(NOT TARGET kos_demo_ui)
    add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../../shared/demo-ui ${CMAKE_CURRENT_BINARY_DIR}/demo-ui)
endif()
kos_add_application(kos-weather
    APP_ID org.nextks.weather
    URI Kos.Apps.Weather
    DISPLAY_NAME "KOS Weather"
    DESKTOP_FILE ${CMAKE_CURRENT_SOURCE_DIR}/data/kos-weather.desktop.in
    ICON_FILE ${CMAKE_CURRENT_SOURCE_DIR}/data/kos-weather.svg
    METAINFO_FILE ${PROJECT_SOURCE_DIR}/packaging/flatpak/org.nextks.weather.metainfo.xml.in
    SOURCES
        src/main.cpp
    QML_SOURCES
        src/WeatherClient.cpp
        src/WeatherClient.h
    QML_FILES
        qml/Main.qml
        qml/WeatherIcon.qml
        qml/WeatherLoadingIndicator.qml
        qml/SnowGlass.qml
    LINK_LIBRARIES
        kos_demo_ui
        kos_demo_ui_plugin
        Qt6::Network
)

# Qt's generated QML type registrar includes native element headers by their
# basename, so expose this app's private source directory to that target.
target_include_directories(kos-weather PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)
if(KOS_FLATPAK_BUILD)
    target_compile_definitions(kos-weather PRIVATE KOS_WEATHER_SANDBOX=1)
endif()
add_dependencies(kos-weather kos-weather-backend-build)
target_compile_definitions(kos-weather PRIVATE
    KOS_WEATHER_BACKEND_BUILD_PATH="${KOS_WEATHER_BACKEND_EXECUTABLE}"
    KOS_WEATHER_BUILD_APP_DIR="${CMAKE_CURRENT_BINARY_DIR}"
)

# 批 7/11｜雪粒子 sprite（程序化生成，无外部美术资源）；雨 sprite 已随批 11
# 删除下落雨粒子层一并移除。与 QML 模块同前缀打包。
# 批 12｜雨改折射：drop-offset.png（偏移图，PIL 脚本生成）+ 折射 shader。
qt_add_resources(kos-weather "weather_particles"
    PREFIX "/qt/qml/Kos/Apps/Weather"
    BASE ${CMAKE_CURRENT_SOURCE_DIR}
    FILES
        qml/particles/snow.png
        qml/particles/drop-offset.png
        qml/shaders/rain_refract.vert.qsb
        qml/shaders/rain_refract.frag.qsb
        qml/shaders/snow_glass.vert.qsb
        qml/shaders/snow_glass.frag.qsb
)
endif()
