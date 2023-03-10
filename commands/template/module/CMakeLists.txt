project(module)

# static module library
add_library(module STATIC 
    src/module.cpp
)
target_include_directories(module 
    PUBLIC include
)

# module unit tests
add_executable(test_module 
    test/test_module.cpp
)
target_link_libraries(test_module
    PRIVATE module
    PRIVATE gtest::gtest
)
