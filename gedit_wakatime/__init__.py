
__version__ = '0.1.0'

import time
import subprocess

from gi.repository import GObject, Gedit

ACTION_FREQUENCY = 2
PLUGIN_USER_AGENT = 'gedit/3 gedit-wakatime/{}'.format(__version__)

_documents = []
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

def get_project_name(file_uri):
    return ''

def send_heartbeat(file_uri, write=False):
    print('Sending heartbeat')
    now = time.time()
    if enough_time_passed(now):
        waka_args = {
            '--file': file_uri,
            '--time': now,
            '--write': write,
            '--plugin': PLUGIN_USER_AGENT,
            '--project': get_project_name(file_uri),
            '--key': None,
        }
        waka_args = ['wakatime'] + flatten_args(waka_args)
        print('Calling wakatime with: {}'.format(waka_args))
        subprocess.call(waka_args)

class WakatimePlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "WakatimePlugin"

    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self._bind_window()

    def do_deactivate(self):
        pass

    def do_update_state(self):
        pass

    def _bind_window(self):
        self._bind_tab(self.window.get_active_tab())
        self.window.connect('active-tab-changed', self._on_active_tab_changed)

    def _on_active_tab_changed(self, window, tab):
        self._bind_tab(tab)

    def _bind_tab(self, tab):
        global _documents
        doc = tab.get_document()
        if doc not in _documents:
            _documents.append(doc)
            doc.connect('saved', self.on_document_saved)
            doc.connect('cursor-moved', self.on_document_changed)

    def on_document_saved(self, document, data=None):
        file_uri = document.get_uri_for_display()
        print('Document saved: {}'.format(file_uri))
        send_heartbeat(file_uri, write=True)

    def on_document_changed(self, document, data=None):
        file_uri = document.get_uri_for_display()
        print('Document changed: {}'.format(file_uri))
        send_heartbeat(file_uri)

