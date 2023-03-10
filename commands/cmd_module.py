from conan.api.conan_api import ConanAPI
from conan.api.output import ConanOutput, Color
from conan.cli.command import OnceArgument, conan_command
from conans.client.userio import UserInput
import os
import re
import subprocess
import shutil
import datetime

# conan path/
home = os.path.expanduser('~')
template_path = f'{home}/.conan2/extensions/commands/template/module'


def copy_template(template_path: str, path: str, module: str):
    date = datetime.datetime.now()
    with open(template_path) as file:
        contents = file.read()
    contents = re.sub('date', date.strftime("%Y/%m/%d"), contents)
    contents = re.sub('module', module, contents)
    with open(path, 'w') as file:
        file.write(contents)


def generate_module(module_path: str):

    (dirname, module) = os.path.split(module_path)

    # 如果路径也存在 那么就创建相应的模块

    # 然后我们需要创建一个模板文件，这个模块文件最好是放在这个仓库里面
    # 这样我们就可以直接复制过去了
    # ../module_name
    #       include/module_name
    #           module_name.hpp
    #       src
    #           module_name.cpp
    #       test
    #           test_module_name.cpp
    #       CMakeLists.txt
    # 我们已经创建好了模板文件 现在我们要做的就是将模板文件整个拷贝到目标目录
    # shutil.copytree(os.path.join('template', 'module'), args)
    # 然后对目标路径下面的所有{module}都修改为用户提供的模块名
    # module/include/module -> module/include/hello
    # shutil.move(os.path.join(args, 'include', 'module'),
    #             os.path.join(args, 'include', module))
    # 然后是修改头文件名
    # 不对 先修改文件内容
    # 还得创建必要的目录
    # module_path = path
    include_path = os.path.join(module_path, 'include', module)
    source_path = os.path.join(module_path, 'src')
    test_path = os.path.join(module_path, 'test')
    # 如果这个模块已经存在了 那么覆写是很危险的
    # 所以如果目录确实已经存在了 那么我们确实不应该再次操作
    # 1. 目录不存在
    # 2. 目录存在 但是是空目录
    # 这两种情况下我们都可以为其生成模块模板 否则拒绝生成 万一覆写文件 非常可怕
    if os.path.exists(module_path):
        if os.path.isfile(module_path):
            print(f"{module_path} is file, cannot mkdir for it")
            return
        if os.listdir(module_path):
            print(
                f"{module_path} is not empty dir, so we could not generate template for it")
            return
    else:
        # 如果不存在那么很简单 就创建一个
        os.mkdir(module_path)

    # os.mkdir(os.join(module, 'include'))
    # mkdir recursively
    os.makedirs(include_path)
    os.mkdir(source_path)
    os.mkdir(test_path)

    template_header = os.path.join(template_path, 'module.hpp')
    template_source = os.path.join(template_path, 'module.cpp')
    template_test = os.path.join(template_path, 'test_module.cpp')
    template_cmake = os.path.join(template_path, 'CMakeLists.txt')

    header = os.path.join(include_path, f'{module}.hpp')
    source = os.path.join(source_path, f'{module}.cpp')
    test = os.path.join(test_path, f'test_{module}.cpp')
    cmake = os.path.join(module_path, 'CMakeLists.txt')

    copy_template(template_header, header, module)
    copy_template(template_source, source, module)
    copy_template(template_test, test, module)
    copy_template(template_cmake, cmake, module)

    # 还有一个问题 如果我们的父目录没有CMakeLists.txt 那么我们需要为其创建一个
    # 这就要求父目录不能是根目录 也就是 .
    if dirname == '.':
        return

    prev_cmake = os.path.join(dirname, 'CMakeLists.txt')
    if os.path.exists(prev_cmake):
        # 在这种情况下我们只需要在最后添加上一行代码即可
        # add_subdirectory(module)
        with open(prev_cmake, 'a') as file:
            file.write(f"add_subdirectory({module})\n")
    else:
        # 在这种情况下我们需要创建这个文件
        with open(prev_cmake, 'w') as file:
            file.write(f"add_subdirectory({module})\n")


@conan_command(group="Custom commands")
def module(conan_api: ConanAPI, parser, *args):
    """
    创建一个子模块
    conan module path1/path2/path3/module_name
    只要path1/path2/path3都存在 那么我们会在path3下面创建一个module_name 并自动创建
    一个可以编译的hello world程序 并且自动创建CMakeLists.txt 并且自动填充上层CMakeLists
    """
    out = ConanOutput()
    if not os.path.exists("conanfile.py"):
        out.error("conanfile.py not found")
        return

    parser.add_argument('-p', '--path', default='', action=OnceArgument,
                        help='path from current path to module name')
    args = parser.parse_args(*args)

    # 用户输入的参数 表示的是从根目录开始 到你希望创建的模块的路径
    path = args.path

    # 用户必须提供相对路径
    if os.path.isabs(path):
        print("must provide a relative path")
        return

    (dirname, basename) = os.path.split(path)

    # 如果tail是空的 那么就不行 用户必须要提供模块的名字
    if not basename:
        print("please input the module name")
        return

    # 如果head是空的 那么 给用户一个提示 一般而言子模块应该在二级目录下面
    # 但是如果用户真的想这么干 我们也不能拦着
    if not dirname:
        # 我们让dirname代表当前路径
        dirname = '.'
        print("normaly module should in a sub folder")

    # 检查提供的路径是否存在
    if not os.path.exists(dirname):
        print(f"path:{path} not exists")
        return

    # 现在path绝对带着一个/
    # 最起码是 ./src
    generate_module(os.path.join(dirname, basename))
