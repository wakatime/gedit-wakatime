#!/usr/bin/python3
from sys import implementation
from setuptools import setup

arch = implementation._multiarch
datadir = '/usr/lib/' + arch + '/gedit/plugins'

setup(
    name="gedit-wakatime",
    version="1.0.1",
    description="Gedit 3.8+ plugin to quantify your coding at https://wakatime.com",
    author="Ricardo Gemignani",
    author_email="ricardo.gemignani@gmail.com",
    url="https://github.com/wakatime/gedit-wakatime",
    license="BSD-2",

    install_requires=['wakatime'],

    data_files=[(datadir, ['wakatime.plugin']),
                (datadir + '/gedit_wakatime', ['gedit_wakatime/__init__.py',
                                               'gedit_wakatime/_version.py',
                                               'gedit_wakatime/plugin.py',
                                               'gedit_wakatime/wakatime.py'])]
)
