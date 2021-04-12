import os
import logging

from gi.repository import GObject, Gedit

from .wakatime import send_heartbeat

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
        self._documents = []

    def do_activate(self):
        self._bind_window()

    def do_deactivate(self):
        pass

    def do_update_state(self):
        pass

    def _bind_window(self):
        self.window.connect('active-tab-changed', self.on_active_tab_changed)

    def _bind_document(self, doc):
        if doc not in self._documents:
            self._documents.append(doc)
            doc.connect('saved', self.on_document_saved)
            doc.connect('tepl-cursor-moved', self.on_document_changed)

    def _get_file_uri(self, document):
        location = document.get_file().get_location()
        if not location:
            return None
        return location.get_path()

    def on_active_tab_changed(self, window, tab):
        document = tab.get_document()
        self._bind_document(document)

        file_uri = document.get_uri_for_display()
        logger.debug("Tab changed: {}".format(file_uri))
        send_heartbeat(file_uri)

    def on_document_saved(self, document, data=None):
        file_uri = self._get_file_uri(document)
        logger.debug('Document saved: {}'.format(file_uri))
        send_heartbeat(file_uri, write=True)

    def on_document_changed(self, document, data=None):
        file_uri = self._get_file_uri(document)
        logger.debug('Document changed: {}'.format(file_uri))
        send_heartbeat(file_uri)
