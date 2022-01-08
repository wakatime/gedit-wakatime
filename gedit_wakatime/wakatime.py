import os
import time
import logging
import subprocess
from gi import __version__ as gedit_version

from ._version import __version__ as plugin_version

logger = logging.getLogger('gedit-wakatime-plugin')

ACTION_FREQUENCY = 2 * 60
PLUGIN_USER_AGENT = 'gedit/{0} gedit-wakatime/{1}'.format(gedit_version, plugin_version)
WAKATIME_CLI = os.path.join(os.path.realpath(os.environ.get('WAKATIME_HOME') or os.path.expanduser('~')), '.wakatime', 'wakatime-cli')

_last_heartbeat_time = 0
_last_heartbeat_file = None


def should_log(file_uri, now, write):
    return (
        write or
        file_uri != _last_heartbeat_file or
        now - _last_heartbeat_time > ACTION_FREQUENCY
    )


def flatten_args(args_dict):
    return [str(arg) for key, value in args_dict.items() if value for arg in [key, value] if not isinstance(arg, bool)]


def send_heartbeat(file_uri, write=False):
    global _last_heartbeat_time, _last_heartbeat_file
    if file_uri is None:
        return
    logger.debug("Heartbeat triggered")
    now = time.time()
    if not should_log(file_uri, now, write):
        logger.debug("Not necessary to send heartbeat")
        return

    args = [WAKATIME_CLI] + flatten_args({
        '--entity': file_uri,
        '--time': now,
        '--write': write,
        '--plugin': PLUGIN_USER_AGENT,
    })
    logger.debug('Calling wakatime with: {}'.format(args))
    subprocess.Popen(args)
    _last_heartbeat_time = now
    _last_heartbeat_file = file_uri
