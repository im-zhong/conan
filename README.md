# conan

My Conan Custom Commands

# 应该做到的是开箱即用, 如果一个工具做不到开箱即用，反而需要极其复杂的配置甚至还需要用户自己编译，那么这就是不合格的

# todo

1. 加一个insights 可以很方便的看某个文件的insights conan insight <source files...>
2. 加一个类似 rust new library 一样的东西 可以非常方便的添加一个模块 同时生成一个hello_world源文件和CMake文件 并自动修改上层CMakeLists添加子模块
3. 把命令行的接口设计成和rust的cargo一样吧 这样就不需要记住两套逻辑了
4. 提供一个命令 可以检查编译目标文件的所有符号
5. add: conan ut --list，可以列出所有的单元测试，就像pytest --co一样

# install

1. ./install.py

# 项目生命周期

1. 创建项目 `conan new top -d name=example` TODO: 为什么不会自动创建一个文件夹呢 参考cargo new example
2. 安装依赖 `conan install . [--build=missing]`
3. 编译项目 `conan build .`
5. 新建模块 `conan module [-t module|test] src/hello`
6. 编译 `conan build .`
7. 测试 `conan ut -r hello` 或者 `conan ut`
8. 格式化 `conan fmt -p src` 或者 `conan fmt`
9. insight `conan insight -p src/main.cpp`
10. conan profile & option. 所以其实如果你想编译debug或者release
首先你需要在conan_home/profiles里面添加一个 debug 和 release 然后再conan cli中添加
一个参数 -pr debug, -pr release 即可
11. 全局的设置是再 conan_home/global.conf里面设置的 [https://docs.conan.io/2/reference/config_files.html]
需要注意的一个点是 当你依赖某些库的时候 需要使用Conan install 进行编译
`conan install -pr release -b missing .`
但是只要这个库被编译好了 其他的项目是不需要这个install过程的 直接build就行

# 真是不容易 终于找到conan怎么查找template路径了 文档写的就是依托

1. apiv2: get_home_template(template_name)
Load a template from the Conan home templates/command/new folder
2. 源代码 conan/conan/cli/commands/new.py
`files = conan_api.new.get_template(args.template)  # First priority: user folderr
    if not files:  # then, try the templates in the Conan home
        files = conan_api.new.get_home_template(args.template)
    if files:
        template_files, non_template_files = files
    else:
        template_files = conan_api.new.get_builtin_template(args.template)
        non_template_files = {}
        `
那我们可以看到 conan会先去当前目录查找，然后去home目录查找 而home目录实际上是 ~/.conan2/templates/command/new
在这个目录下面放自己的template 比如
~/.conan2/templates/command/new/test/xxx.txt
然后 `conan new test -d key=value ...`

# 增加两个命令

1. conan st <path> 借助自己的code statistics 工具统计代码量 conan status .
2. 如果src内部存在一个main文件夹 那么conan可以认为这个main里面存放着一个可执行文件 那么 conan run {args...} 就会用args调用该可执行文件

# 调研cargo的命令行和项目组织方式，取其精华

# 分两种 一种是创建整个项目 conan new 对应 cargo new --lib --bin

# 第二种是增加一个新的模块 conan mod 对应 cargo 没有 cargo的mod创建起来非常简单 所以都是直接创建一个文件

1. conan mod --lib include/ src/ test/
2. conan mod --bin bin.cpp
3. conan mod --test test.cpp doctest
lib bin example bench test

conan clean 对应 cargo clean
conan build 对应 cargo build
conan run 对应 cargo run, 感觉conan run 可以代替 conan ut conan run test 可以用subcommand实现
conan fmt
conan perf
conan stat
conan insight

<https://docs.conan.io/2.0/reference/extensions/custom_commands.html>

# <https://docs.conan.io/2.0/reference/extensions/custom_commands.html#argument-definition-and-parsing>

argparse
