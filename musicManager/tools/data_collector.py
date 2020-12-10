import json
import logging
from os import path
from time import time


# TODO: fix issue where the last played media doesnt get saved because while exiting log_play_percentage isn't called
class data_collector:
    def __init__(self, logger: logging, USER_DATA_DIR: str):
        """
        Collects usage data to later on suggest songs... (to be implemented)
        """

        self.logger = logger
        self.DATA_DIR = USER_DATA_DIR
        self.data_filename = path.join(USER_DATA_DIR, "data.json")

        self.start_time = time()

        self._current_playlist = ""
        self._start_playlist_time = 0

        self._init()

    # initial setup of necessary variables
    def _init(self):
        self.logger.info("Initializing data collection")

        # if ~/.musicManager/data/data.json doesnt exist:
        if not path.isfile(self.data_filename):
            self._initial_setup()

        self.data_file = open(self.data_filename, "r+")

        self.playlist_playtimes = json.load(self.data_file)["playlist_playtimes"]
        self.data_file.seek(0)

        self.play_percentage = json.load(self.data_file)["play_percentage"]
        self.data_file.seek(0)

    # creates ~/.musicManager/data/data.json and adds default information
    def _initial_setup(self):

        _default_data = {
            "playing_time": 0,  # in seconds
            "playlist_playtimes": {},
            "genre_playtimes": {},
            "play_percentage": {}
        }

        with open(self.data_filename, "w") as file:
            json.dump(_default_data, file, ensure_ascii=False, indent=4)

    def log_info(self, msg: str):
        self.logger.info(msg)

    # logs critical information, saves all collected data and then exists
    def log_and_exit(self, msg: str, exit_code=0):
        from .cli import show_cursor
        show_cursor()

        self.logger.critical(msg)
        self._exit_operations()
        exit(exit_code)

    def log_play_percentage(self, filename: str, percent: int):
        if filename in self.play_percentage: self.play_percentage[filename].append(percent)
        else: self.play_percentage[filename] = [percent]

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
        json_data["play_percentage"] = self.play_percentage
        json_data["playlist_playtimes"] = self.playlist_playtimes
        self.data_file.close()

        with open(self.data_filename, "w") as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)