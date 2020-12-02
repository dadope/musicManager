import json
from os import path
from glob import glob

from ..constants import PLAYLISTS_DIR

def getPlaylists() -> list:
    """
    Loads all playlists from .../project_install_dir/res/playlists
    json file format =>
    {
        "playlist": "<name of the specific playlist>",
        "genre": "<genre '''>",
        "dir": "<directory to search for all the files>"
    }
    """

    return  [json.load(open(x, "r")) for x in glob(path.join(PLAYLISTS_DIR, "*.json"))]

def getSongs(playlists:dict) -> list:
    """
    return all the mp3 files in the playlists directory

    :param playlists: playlist to get the songs from
    :return: a list of all mp3 files in the playlists directory
    """

    return [x for x in glob(path.join(playlists["directory"], "*.mp3"))]
