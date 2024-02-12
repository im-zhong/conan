from conan.api.conan_api import ConanAPI
from conan.api.output import ConanOutput, Color
from conan.cli.command import OnceArgument, conan_command
from conans.client.userio import UserInput
import os
import subprocess


def dofmt(out: ConanOutput, path: str):
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith((".h", "hh", ".hpp", ".c", ".cxx", ".cpp")):
                filename = os.path.join(root, file)
                out.info(f"formatting... {filename}")
                result = subprocess.run(
                    ["clang-format", "-i", filename],
                    capture_output=True,
                    encoding="utf-8",
                )
                if result.stdout:
                    out.info(result.stdout)
                if result.stderr:
                    out.error(result.stderr)


@conan_command(group="Custom commands")
def fmt(conan_api: ConanAPI, parser, *args):
    """
    Use clang-format to fmt directory
    """

    out = ConanOutput()
    if not os.path.exists("conanfile.py"):
        out.error("conanfile.py not found")
        return
    if not os.path.exists(".clang-format"):
        out.error(".clang-format not found")
        return

    parser.add_argument("path", help="path")
    args = parser.parse_args(*args)

    if not args.path:
        dofmt(out, os.path.curdir)
    else:
        dofmt(out, args.path)
