from pynput.keyboard import Listener

from .handler import mediaHandler
from ..constants import PAUSE_MEDIA_KEY, NEXT_MEDIA_KEY, PREV_MEDIA_KEY, STOP_MEDIA_KEY, collector

class listener:
    def __init__(self, handler: mediaHandler):
        """
        listens to user input and executes commands respectively

        :param handler: media handler to be used
        """

        self.handler = handler

    def _on_press(self, key):
        """
        Key press parser

        :param key: key that is pressed
        """

        if str(key) == PAUSE_MEDIA_KEY:
            self.handler.play_pause()
        if str(key) == NEXT_MEDIA_KEY:
            collector.log_info("Skipping a track")
            self.handler.next()
        if str(key) == PREV_MEDIA_KEY:
            collector.log_info("Returning to previous track")
            self.handler.previous()
        if str(key) == STOP_MEDIA_KEY:
            print("Stop media key pressed, exiting")
            collector.log_critical_and_exit("Stop media key pressed, exiting")

    def startListening(self):
        """
        Starts the thread
        """

        listener_thread = Listener(on_press=self._on_press)
        listener_thread.start()
        listener_thread.join()