gedit-wakatime
============

Gedit 3.8+ plugin to quantify your coding at https://wakatime.com

This plugin was contributed by WakaTime community member [Ricardo Gemignani](https://github.com/rsgemignani).


Download
--------

See [GitHub releases](https://github.com/wakatime/gedit-wakatime/releases)


Installation
------------

1. Run the `install.py` script as root
2. Edit `~/.wakatime.cfg` and add your apikey as follows:

    ```
    [settings]
    api_key = <your-api-key>
    ```
3. Activate the plugin in Gedit Edit > Preferences > Plugins


Note: If your Gedit plugins directory is non-standard pass it to `install.py` like:

    sudo ./install.py ~/.gnome2/gedit/plugins/


Screen Shots
------------

![Project Overview](https://wakatime.com/static/img/ScreenShots/ScreenShot-2014-10-29.png)
