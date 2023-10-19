from conan.api.conan_api import ConanAPI
from conan.api.output import ConanOutput, Color
from conan.cli.command import OnceArgument, conan_command
from conans.client.userio import UserInput
import os
import re
import subprocess
import time

# TIP1: 把chrome加到windows path里面，这样就可以从wsl里面启动了
# 或者把 explorer.exe alias 成 open 然后把svg的默认打开程序设置为chrome
# 也可以直接 open *.svg
# 果然这样就可以了
# TIP2: 在wsl上安装perf
# https://gist.github.com/abel0b/b1881e41b9e1c4b16d84e5e083c38a13
# TIP3: how to use perf and frame graph
# https://github.com/brendangregg/FlameGraph
# clone这个仓库并且将这些脚本放到path里面
# perf record -g <cmd> > perf.data
# perf script -i perf.data -o yyy.perf
# stackcollapse-perf.pl yyy.perf > in-fb.folded
# flamegraph.pl in-fb.folded > in-fb-cpu.svg


@conan_command(group="Custom commands")
def perf(conan_api: ConanAPI, parser, *args):
    """
    perf executable file
    """

    out = ConanOutput()
    if not os.path.exists("conanfile.py"):
        out.error("conanfile.py not found")
        return

    # args = parser.parse_args(*args)
    # conan perf <name, path>
    # <name>.data
    # <name>.perf
    # <name>.folded
    # <name>.svg

    parser.add_argument('regex', help='search unit test witl regex')
    args = parser.parse_args(*args)

    # 查找所有以test_开头的可执行程序 并且执行
    # 还是给出正则表达式吧
    for root, _, files in os.walk("build/Debug"):
        for file in files:
            if args.regex and not re.search(args.regex, file):
                continue
            filename = os.path.join(root, file)
            if os.access(filename, os.X_OK):
                print(f"perf... {filename}")

                # mode=w means truncate
                subprocess.run(
                    ['perf', 'record', '-g', '-o', 'tmp.data', filename])
                with open('tmp.perf', 'w') as f:
                    subprocess.run(
                        ['perf', 'script', '-i', 'tmp.data'], stdout=f)
                with open('tmp.folded', 'w') as f:
                    subprocess.run(
                        ['stackcollapse-perf.pl', 'tmp.perf'], stdout=f)
                with open('tmp.svg', 'w') as f:
                    subprocess.run(
                        ['flamegraph.pl', 'tmp.folded'], stdout=f)

                # 只考虑匹配到的第一个程序
                return
