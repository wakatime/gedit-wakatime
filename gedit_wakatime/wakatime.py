import time
import subprocess

from ._version import __version__

ACTION_FREQUENCY = 2
PLUGIN_USER_AGENT = 'gedit/3 gedit-wakatime/{}'.format(__version__)

_last_heartbeat = 0

def enough_time_passed(now, last_time=None):
    if not last_time:
        last_time = _last_heartbeat
    if now - last_time > ACTION_FREQUENCY * 60:
        return True
    return False

def flatten_args(args_dict):
    return [str(arg) for key, value in args_dict.items() if value
                for arg in [key, value] if not isinstance(arg, bool)]

def send_heartbeat(file_uri, write=False):
    print('Sending heartbeat')
    now = time.time()
    if enough_time_passed(now):
        waka_args = {
            '--file': file_uri,
            '--time': now,
            '--write': write,
            '--plugin': PLUGIN_USER_AGENT,
        }
        waka_args = ['wakatime'] + flatten_args(waka_args)
        print('Calling wakatime with: {}'.format(waka_args))
        subprocess.call(waka_args)
        global _last_heartbeat
        _last_heartbeat = now

