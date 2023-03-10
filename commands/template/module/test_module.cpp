// date

#include "module/module.hpp"
#include "gtest/gtest.h"

int main(int argc, char *argv[]) {
  EXPECT_EQ(module::HelloWorld(), "hello, world");
}
