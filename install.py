#!/usr/bin/env python3

import sys
import shutil
import subprocess
from os import path

base_path = path.dirname(path.abspath(__file__))

gedit_plugins_dir = '/usr/lib/gedit/plugins'

plugin_module_name = 'gedit_wakatime'
plugin_module_src_dir = path.join(base_path, plugin_module_name)
plugin_module_dst_dir = path.join(gedit_plugins_dir, plugin_module_name)

plugin_descriptor_fname = 'wakatime.plugin'
plugin_descriptor_file = path.join(base_path, plugin_descriptor_fname)

def install():
    try:
        if path.exists(plugin_module_dst_dir):
            shutil.rmtree(plugin_module_dst_dir)
        shutil.copytree(plugin_module_src_dir, plugin_module_dst_dir)
        shutil.copy(plugin_descriptor_file, gedit_plugins_dir)
        print('Wakatime plugin installation successful.')
        print('Now activate it in gedit Edit > Preferences > Plugins.')
    except PermissionError:
        print('ERROR: You must be root.')
        print('Try: sudo {}'.format(' '.join(sys.argv)))

if __name__ == '__main__':
    install()

