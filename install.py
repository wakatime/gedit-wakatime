#!/usr/bin/env python3

import sys
import shutil
from os.path import abspath, dirname, exists, expanduser, join

sys.path.insert(0, abspath('.'))
from install_cli import main as install_cli

base_path = dirname(abspath(__file__))
home_dir = expanduser('~')

if sys.argv[1:]:
    gedit_plugins_dir = expanduser(sys.argv[1])
else:
    gedit_plugins_dir = join(home_dir, '.local', 'share', 'gedit', 'plugins')

plugin_module_name = 'gedit_wakatime'
plugin_module_src_dir = join(base_path, plugin_module_name)
plugin_module_dst_dir = join(gedit_plugins_dir, plugin_module_name)

plugin_descriptor_fname = 'wakatime.plugin'
plugin_descriptor_file = join(base_path, plugin_descriptor_fname)


try:
    assert PermissionError
except:
    class PermissionError(Exception):
        pass


def install():
    install_cli()
    if exists(plugin_module_dst_dir):
        shutil.rmtree(plugin_module_dst_dir)
    shutil.copytree(plugin_module_src_dir, plugin_module_dst_dir)
    shutil.copy(plugin_descriptor_file, gedit_plugins_dir)
    print('Wakatime plugin installation successful.')
    print('Now activate it in gedit Edit > Preferences > Plugins.')


if __name__ == '__main__':
    try:
        install()
    except (PermissionError, IOError, OSError):
        print('ERROR: You must be root.')
        print('Try: sudo {}'.format(' '.join(sys.argv)))
