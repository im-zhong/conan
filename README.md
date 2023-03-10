# conan
My Conan Custom Commands

# 应该做到的是开箱即用, 如果一个工具做不到开箱即用，反而需要极其复杂的配置甚至还需要用户自己编译，那么这就是不合格的

# todo
1. 加一个insights 可以很方便的看某个文件的insights conan insight <source files...>
2. 加一个类似 rust new library 一样的东西 可以非常方便的添加一个模块 同时生成一个hello_world源文件和CMake文件 并自动修改上层CMakeLists添加子模块 

# install
1. ./install.py

# 项目生命周期
1. 创建项目 `conan new cmake_exe -d name=example -d version=0.1 -d requires=gtest/cci.20210126`
2. 安装依赖 `conan install . --build=missing`
3. 替换顶层目录模板文件 `conan top`, 将template/top文件夹内的文件与项目目录顶层文件夹内的文件进行替换
4. 删除项目模板带着无用的文件 `rm -rf src/*`
5. 新建模块 `conan module -p src/hello`
6. 编译 `conan build .`
7. 测试 `conan ut -r hello` 或者 `conan ut`

# 真是不容易 终于找到conan怎么查找template路径了 文档写的就是依托
1. apiv2: get_home_template(template_name)
Load a template from the Conan home templates/command/new folder
2. 源代码 conan/conan/cli/commands/new.py 
`    files = conan_api.new.get_template(args.template)  # First priority: user folder
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