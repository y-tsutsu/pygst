cmake_minimum_required(VERSION 2.8)
add_definitions("-Wall -std=c++11")
set(CMAKE_BUILD_TYPE Debug)

find_package(PkgConfig)
pkg_check_modules(LIBGSTREAMER REQUIRED gstreamer-1.0)
include_directories(${LIBGSTREAMER_INCLUDE_DIRS})
link_directories(${LIBGSTREAMER_LIBRARY_DIRS})

add_executable(tuto01
    tuto01.c
)

target_link_libraries(tuto01
    ${LIBGSTREAMER_LIBRARIES}
)
