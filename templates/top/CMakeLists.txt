cmake_minimum_required(VERSION 3.25.0)
project({{name}} CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED on)
set(CMAKE_EXPORT_COMPILE_COMMANDS on)

find_package(fmt REQUIRED)
find_package(GTest REQUIRED)

add_subdirectory(src)
