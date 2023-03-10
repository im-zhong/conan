#!/usr/bin/env python
# 2023/3/10

import shutil
import os

home = os.path.expanduser('~')
conan_home = f'{home}/.conan2'
commands_path = f'{conan_home}/extensions/commands'
templates_path = f'{conan_home}/templates/command/new'

shutil.copytree(
    './commands', commands_path, dirs_exist_ok=True)
shutil.copytree(
    './templates', templates_path, dirs_exist_ok=True
)
