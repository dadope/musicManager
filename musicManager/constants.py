import json
import logging
import pathlib

from shutil import move
from os import path, mkdir, remove

# user home directory
_user_home = str(pathlib.Path.home())

# project resource directory (.../home/.musicManager/)
PROJECT_DATA_DIR = path.join(_user_home, ".musicManager")

RES_DIR = path.join(PROJECT_DATA_DIR, "res")
PLAYLISTS_DIR = path.join(RES_DIR, "playlists")
USER_DATA_DIR = path.join(PROJECT_DATA_DIR, "data")

# music directory (.../home/Music/)
MUSIC_DIR = path.join(_user_home, "Music")

# setting up all important directories in case PROJECT_DATA_DIR doesnt exist
if not path.exists(PROJECT_DATA_DIR):
    mkdir(PROJECT_DATA_DIR)

    # directory in which the project is currently located
    _current_project_dir = path.dirname(path.realpath(__file__))

    remove(path.join(_current_project_dir, "res", "playlists", "deleteme"))

    move(path.join(_current_project_dir, "data"), PROJECT_DATA_DIR)
    move(path.join(_current_project_dir, "res"), PROJECT_DATA_DIR)


    #TODO: make the user select the default playlist

    from .tools import indexer

    _default_playlist = indexer.index_music(MUSIC_DIR, PLAYLISTS_DIR)

    #TODO: make user setup his media keys

    _default_settings = {
      "default_playlist": _default_playlist,
      "default_playback_order": "random",

      "next_media_key": "<269025047>",
      "prev_media_key": "<269025046>",
      "stop_media_key": "<269025045>",
      "pause_media_key": "<269025044>"
    }

    with open(path.join(USER_DATA_DIR, "settings.json"), "w") as file:
        json.dump(_default_settings, file, ensure_ascii=False, indent=4)

# loading settings from (.../home/.musicManager/data/settings.json)
SETTINGS = json.load(open(path.join(USER_DATA_DIR, "settings.json"), "r"))

# reading default media key values from the settings
NEXT_MEDIA_KEY = SETTINGS["next_media_key"]
PREV_MEDIA_KEY = SETTINGS["prev_media_key"]
STOP_MEDIA_KEY = SETTINGS["stop_media_key"]
PAUSE_MEDIA_KEY = SETTINGS["pause_media_key"]

# setting up the logger (log file: .../home/.musicManager/data/logs.log)
logger = logging
logger.basicConfig(filename=path.join(USER_DATA_DIR, "logs.log"), level=logging.INFO, format="%(asctime)s => %(name)s:%(process)d :: (%(levelname)s) %(message)s")