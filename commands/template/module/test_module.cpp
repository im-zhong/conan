// date

#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest/doctest.h"
#include "module/module.hpp"
#include <iostream>

TEST_CASE("testing module") { std::cout << "hello module" << std::endl; }
