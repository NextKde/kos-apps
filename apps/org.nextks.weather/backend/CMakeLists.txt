find_program(GO_EXECUTABLE go REQUIRED)
execute_process(COMMAND ${GO_EXECUTABLE} version OUTPUT_VARIABLE GO_VERSION OUTPUT_STRIP_TRAILING_WHITESPACE)
if(NOT GO_VERSION MATCHES "go([0-9]+)\\.([0-9]+)" OR CMAKE_MATCH_1 LESS 1 OR (CMAKE_MATCH_1 EQUAL 1 AND CMAKE_MATCH_2 LESS 22))
    message(FATAL_ERROR "Go 1.22 or newer is required; found ${GO_VERSION}")
endif()
set(KOS_WEATHER_BACKEND_EXECUTABLE ${CMAKE_CURRENT_BINARY_DIR}/kos-weather-backend PARENT_SCOPE)
file(GLOB backend_sources CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/*.go)
add_custom_command(OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/kos-weather-backend
    COMMAND ${CMAKE_COMMAND} -E env GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off CGO_ENABLED=0
        ${GO_EXECUTABLE} build -mod=readonly -trimpath -buildvcs=false -o ${CMAKE_CURRENT_BINARY_DIR}/kos-weather-backend .
    DEPENDS ${backend_sources} ${CMAKE_CURRENT_SOURCE_DIR}/go.mod
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    VERBATIM)
add_custom_target(kos-weather-backend-build ALL DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/kos-weather-backend)
install(PROGRAMS ${CMAKE_CURRENT_BINARY_DIR}/kos-weather-backend DESTINATION ${CMAKE_INSTALL_BINDIR})
if(BUILD_TESTING)
    add_test(NAME kos-weather.backend
        COMMAND ${CMAKE_COMMAND} -E env GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off
            ${GO_EXECUTABLE} test -mod=readonly ./...)
    set_tests_properties(kos-weather.backend PROPERTIES
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} LABELS data TIMEOUT 60)
endif()
