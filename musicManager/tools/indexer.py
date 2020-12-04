import glob
import json
from os import path

def index_music(MUSIC_DIR:str, PLAYLISTS_DIR:str):
    """
    Takes every folder (with at least 1 mp3 file in it) in the users music directory and indexes it into specific playlists depending on the folder

    :return: the last created playlist
    """

    playlists = []
    number_of_playlists = 0

    print("Indexing music...\n\n")

    # for folder in the music directory do
    for folder in glob.glob(path.join(MUSIC_DIR, "*/")):

        # confirms that mp3 files are in the folder
        if len(glob.glob(path.join(folder, "*.mp3"))) != 0:
            # removes the trailing / and gets the folder name
            playlist_name = path.basename(path.normpath(folder))
            playlists.append(playlist_name)

            number_of_playlists =+ 1
            print(f"found music in '{folder}', adding as playlist\n")

            playlist_json = {
                "playlist": playlist_name,
                "directory": folder
            }

            with open(path.join(PLAYLISTS_DIR, playlist_name + ".json"), "w") as file:
                json.dump(playlist_json, file, ensure_ascii=False, indent=4)

    if number_of_playlists == 0:
        print("WARNING!\ncould not find any playlists in your music folder that contain an mp3 file, please manually add your playlists and then run the program again")
        exit(1)

    return playlists