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

        self._init()

    # initial setup of necessary variables
    def _init(self):
        self.logger.info("Initializing data collection")

        try:
            self.data_file = open(self.data_filename, "r+")

        # if ~/.musicManager/data/data.json doesnt exist, do:
        except FileNotFoundError:
            self._initial_setup()
            self.data_file = open(self.data_filename, "r+")

    # creates ~/.musicManager/data/data.json and adds default information
    def _initial_setup(self):

        _default_data = {
            "playing_time": 0  # in seconds
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

    # collects and saves all data in ~/.musicManager/data/data.json
    def _exit_operations(self):
        run_time = int(time() - self.start_time)

        json_data = json.load(self.data_file)
        json_data["playing_time"] += run_time

        self.data_file.close()
        with open(self.data_filename, "w") as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)
