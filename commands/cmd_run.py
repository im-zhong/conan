from conan.api.conan_api import ConanAPI
from conan.api.output import ConanOutput, Color
from conan.cli.command import OnceArgument, conan_command
from conans.client.userio import UserInput
import os
import re
import subprocess
import time


@conan_command(group="Custom commands")
def run(conan_api: ConanAPI, parser, *args):
    """
    run executable file
    """

    out = ConanOutput()
    if not os.path.exists("conanfile.py"):
        out.error("conanfile.py not found")
        return

    # args = parser.parse_args(*args)

    for root, _, files in os.walk("build/Debug/src"):
        for file in files:
            filename = os.path.join(root, file)
            if os.access(filename, os.X_OK):
                # 这里还需要收集返回的信息
                # out.info(f"running... {filename}")
                # print(args)

                # 把args作为filename的参数进行调用
                commands = [filename]
                # 把args的内容添加到commands中
                for arg in args:
                    # print(arg)
                    for a in arg:
                        commands.append(a)
                # print(commands)
                # join commands
                cmd = ""
                for c in commands:
                    cmd += c + " "
                out.info(f"running... {cmd}\n")
                result = subprocess.run(commands, capture_output=True, encoding="utf-8")

                if result.stdout:
                    out.info(result.stdout)
                if result.stderr:
                    out.error(result.stderr)
