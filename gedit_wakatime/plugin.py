import os
import logging

from gi.repository import GObject, Gedit

from .wakatime import send_heartbeat

_documents = []

logger = logging.getLogger('gedit-wakatime-plugin')
logger.addHandler(logging.StreamHandler())
if os.environ.get('GEDIT_WAKATIME_PLUGIN_DEBUG'):
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.WARN)

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
        logger.debug('Document saved: {}'.format(file_uri))
        send_heartbeat(file_uri, write=True)

    def on_document_changed(self, document, data=None):
        file_uri = document.get_uri_for_display()
        logger.debug('Document changed: {}'.format(file_uri))
        send_heartbeat(file_uri)

