from conan.api.conan_api import ConanAPI
from conan.api.output import ConanOutput, Color
from conan.cli.command import OnceArgument, conan_command
from conans.client.userio import UserInput
import os
import re
import subprocess
import time


@conan_command(group="Custom commands")
def ut(conan_api: ConanAPI, parser, *args):
    """
    automatically run unit test
    """

    out = ConanOutput()
    if not os.path.exists("conanfile.py"):
        out.error("conanfile.py not found")
        return

    parser.add_argument('regex', help='search unit test witl regex')
    parser.add_argument('-t', '--timeout', default='60',
                        action=OnceArgument, help='timeout for each test')
    parser.add_argument('-m', '--memcheck', default='false',
                        action=OnceArgument, help='check with valgrind --tool=memcheck')
    args = parser.parse_args(*args)

    failed_list = []
    n = 1
    passed = 0
    failed = 0
    start_time = time.time()
    # 查找所有以test_开头的可执行程序 并且执行
    # 还是给出正则表达式吧
    for root, _, files in os.walk("build"):
        for file in files:
            if file.startswith("test_"):
                if args.regex and not re.search(args.regex, file):
                    continue
                filename = os.path.join(root, file)
                if os.access(filename, os.X_OK):
                    print(f"#{n} testing... {filename}")
                    # 这里还需要收集返回的信息
                    if args.memcheck == 'true':
                        result = subprocess.run(
                            ["valgrind", "--tool=memcheck", filename], capture_output=True, encoding='utf-8', timeout=int(args.timeout))
                    else:
                        result = subprocess.run(
                            [filename], capture_output=True, encoding='utf-8', timeout=int(args.timeout))
                    # 我们还可以收集通过测试的数量
                    if result.returncode == 0:
                        passed += 1
                    else:
                        failed_list.append(filename)
                        failed += 1
                    n += 1
                    if result.stdout:
                        out.info(result.stdout)
                    if result.stderr:
                        out.error(result.stderr)
    end_time = time.time()

    out.info(f"result: {passed}/{n-1} passed, {failed}/{n-1} failed.")
    out.info(f"cost: {end_time - start_time}s")
    # 如果有测试失败的 应当把他们的名字列出来
    if len(failed_list) > 0:
        out.info("failed tests:")
        for failed in failed_list:
            out.info(f"  - {failed}")
