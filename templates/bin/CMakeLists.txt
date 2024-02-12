cmake_minimum_required(VERSION 3.20)
project({{name}} CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED on)
set(CMAKE_EXPORT_COMPILE_COMMANDS on)

find_package(doctest REQUIRED)

# https://cmake.org/cmake/help/latest/command/add_compile_options.html
# https://github.com/doctest/doctest/blob/master/doc/markdown/configuration.md#doctest_config_disable
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    add_compile_options(-DDOCTEST_CONFIG_DISABLE)
endif()

add_subdirectory(src)
add_subdirectory(test)
