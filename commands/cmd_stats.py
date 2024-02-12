from conan.api.conan_api import ConanAPI
from conan.api.output import ConanOutput, Color
from conan.cli.command import OnceArgument, conan_command
from conans.client.userio import UserInput
import os
import subprocess


@conan_command(group="Custom commands")
def stats(conan_api: ConanAPI, parser, *args):
    """
    Use clang-format to fmt directory
    """

    out = ConanOutput()
    # if not os.path.exists("conanfile.py"):
    #     out.error("conanfile.py not found")
    #     return

    parser.add_argument("path", help="path")
    args = parser.parse_args(*args)

    result = subprocess.run(
        ["code_statistics", args.path], capture_output=True, encoding="utf-8"
    )
    if result.stdout:
        out.info(result.stdout)
    if result.stderr:
        out.error(result.stderr)
