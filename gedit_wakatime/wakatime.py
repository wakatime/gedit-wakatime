import time
import logging
import subprocess

from ._version import __version__

logger = logging.getLogger('gedit-wakatime-plugin')

ACTION_FREQUENCY = 2
PLUGIN_USER_AGENT = 'gedit/3 gedit-wakatime/{}'.format(__version__)

_last_heartbeat = {}

def enough_time_passed(now, last_time):
    if now - last_time > ACTION_FREQUENCY * 60:
        return True
    return False

def flatten_args(args_dict):
    return [str(arg) for key, value in args_dict.items() if value
                for arg in [key, value] if not isinstance(arg, bool)]

def send_heartbeat(file_uri, write=False):
    global _last_heartbeat
    logger.debug('Sending heartbeat')
    now = time.time()
    if enough_time_passed(now, _last_heartbeat.get(file_uri, 0)) or write:
        waka_args = {
            '--file': file_uri,
            '--time': now,
            '--write': write,
            '--plugin': PLUGIN_USER_AGENT,
        }
        waka_args = ['wakatime'] + flatten_args(waka_args)
        logger.debug('Calling wakatime with: {}'.format(waka_args))
        subprocess.Popen(waka_args)
        _last_heartbeat[file_uri] = now

