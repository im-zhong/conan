#!/usr/bin/env python
# 2023/3/10

import shutil
import os


def install_commands():
    home = os.path.expanduser('~')
    shutil.copytree(
        './commands', f'{home}/.conan2/extensions/commands', dirs_exist_ok=True)


install_commands()
