# conan
My Conan Custom Commands

# 应该做到的是开箱即用, 如果一个工具做不到开箱即用，反而需要极其复杂的配置甚至还需要用户自己编译，那么这就是不合格的

# todo
1. 加一个insights 可以很方便的看某个文件的insights conan insight <source files...>
2. 加一个类似 rust new library 一样的东西 可以非常方便的添加一个模块 同时生成一个hello_world源文件和CMake文件 并自动修改上层CMakeLists添加子模块 


# 项目生命周期
1. 创建项目 `conan new cmake_exe -d name=hello -d version=0.1`
2. 创建模块 conan module