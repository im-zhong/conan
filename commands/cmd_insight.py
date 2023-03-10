from conan.api.conan_api import ConanAPI
from conan.api.output import ConanOutput, Color
from conan.cli.command import OnceArgument, conan_command
from conans.client.userio import UserInput
import os
import subprocess


@conan_command(group="Custom commands")
def insight(conan_api: ConanAPI, parser, *args):
    """
    automatically run unit test
    """

    # insight 为什么要通过conan来调？？？
    parser.add_argument('-p', '--path', default='', action=OnceArgument,
                        help='cpp file')
    args = parser.parse_args(*args)

    out = ConanOutput()
    result = subprocess.run(["insights", args.path],
                            capture_output=True, encoding="utf-8")
    if result.stdout:
        out.info(result.stdout)
    if result.stderr:
        out.error(result.stderr)
