import json
import logging
from os import path
from time import time

# TODO:add file specific playing time, skip time...
class data_collector:
    def __init__(self, logger: logging, USER_DATA_DIR: str):
        """
        Collects usage data to later on suggest songs... (to be implemented)
        """

        self.logger = logger
        self.DATA_DIR = USER_DATA_DIR
        self.data_filename = path.join(USER_DATA_DIR, "data.json")

        self.start_time = time()

        self._current_song = ""
        self._start_song_time = 0

        self._current_playlist = ""
        self._start_playlist_time = 0

        self._init()

    # initial setup of necessary variables
    def _init(self):
        self.logger.info("Initializing data collection")

        try:
            self.data_file = open(self.data_filename, "r+")

        # if ~/.musicManager/data/data.json doesnt exist:
        except FileNotFoundError:
            self._initial_setup()
            self.data_file = open(self.data_filename, "r+")

        self.playlist_playtimes = json.load(self.data_file)["playlist_playtimes"]
        self.data_file.seek(0)

        self.song_playtimes = json.load(self.data_file)["song_playtimes"]
        self.data_file.seek(0)

    # creates ~/.musicManager/data/data.json and adds default information
    def _initial_setup(self):

        _default_data = {
            "playing_time": 0,  # in seconds
            "playlist_playtimes": {},
            "genre_playtimes": {},
            "song_playtimes": {}
        }

        with open(self.data_filename, "w") as file:
            json.dump(_default_data, file, ensure_ascii=False, indent=4)

    def log_info(self, msg: str):
        self.logger.info(msg)

    # logs critical information, saves all collected data and then exists
    def log_critical_and_exit(self, msg: str, exit_code = 0):
        self.logger.critical(msg)
        self._exit_operations()
        exit(exit_code)

    def start_song_timer(self, filename: str):
        self._current_song = filename
        self._start_song_time = time()

    def stop_song_timer(self):
        if self._current_song is None:
            return

        song_playtime = int(time() - self._start_song_time)

        # confirms that the playlist exists in the list
        if self._current_playlist not in self.song_playtimes:
            self.song_playtimes[self._current_playlist] = {}


        if self._current_song in self.song_playtimes[self._current_playlist]:
            self.song_playtimes[self._current_playlist][self._current_song] += song_playtime

        else: self.song_playtimes[self._current_playlist][self._current_song] = song_playtime

        self._start_song_time = 0
        self._current_song = None


    def start_playlist_timer(self, playlist: str):
        self._current_playlist = playlist
        self._start_playlist_time = time()

    def stop_playlist_timer(self):
        playlist_playtime = int(time() - self._start_playlist_time)

        if self._current_playlist in self.playlist_playtimes:
            self.playlist_playtimes[self._current_playlist] += playlist_playtime

        else: self.playlist_playtimes[self._current_playlist] = playlist_playtime

        self._start_playlist_time = 0


    # collects and saves all data in ~/.musicManager/data/data.json
    def _exit_operations(self):
        run_time = int(time() - self.start_time)

        json_data = json.load(self.data_file)
        json_data["playing_time"] += run_time
        json_data["song_playtimes"] = self.song_playtimes
        json_data["playlist_playtimes"] = self.playlist_playtimes

        self.data_file.close()
        with open(self.data_filename, "w") as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)
