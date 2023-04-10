add_executable(test_module module.cpp)
target_link_libraries(test_module PRIVATE doctest::doctest)
