#TODO: add listening data collection: time listened, tracks skipped...

import argparse

from .constants import SETTINGS, collector
from .tools import listener, other, handler

parser = argparse.ArgumentParser(description="Music player written in python", prog="musicManager")

parser.add_argument("-p", "--playlist",  action="store",     type=str, help="Specify the playlist to play")
parser.add_argument("-a", "--artist",    action="store",     type=str, help="Specify the artist to play")
parser.add_argument("-n", "--alphabet",  action="store_true",          help="play in alphabetic order")
parser.add_argument("-c", "--cli",       action="store_true",          help="display cli information")
parser.add_argument("-r", "--random",    action="store_true",          help="play randomly")

args = parser.parse_args()
playlists = other.getPlaylists()

def main():
    try:
        if args.playlist:
            play(args.playlist)
        else:
            if args.cli:
                print(f"No playlist was selected, falling back to the default playlist... ({SETTINGS['default_playlist']})")
            play(SETTINGS["default_playlist"])
    except KeyboardInterrupt:
        if args.cli:
            print("\nExiting program")
        collector.log_critical_and_exit("Keyboard interrupt pressed, exiting")


def play(inputPlaylist):
    playlist_to_play = None

    for x in playlists:
        if x["playlist"] == inputPlaylist:
            playlist_to_play = x

    if not playlist_to_play:
        print("Error - could not find that playlist, exiting")
        collector.log_critical_and_exit(f"could not find playlist '{inputPlaylist}', exiting", 1)

    # getting a list of all songs in playlist_to_play
    songs = other.getSongs(playlist_to_play)

    # choosing the order in which the elements are played
    if args.random:
        input_listener = listener.listener(handler.mediaHandler(songs, handler.RANDOM_ORDER, args.artist, args.cli))
    elif args.alphabet:
        input_listener = listener.listener(handler.mediaHandler(songs, handler.ALPHABETIC_ORDER, args.artist, args.cli))
    else:
        if args.cli:
            print(f"No playback option was selected, falling back to the default... ({SETTINGS['default_playback_order']})")
        input_listener = listener.listener(handler.mediaHandler(songs, SETTINGS["default_playback_order"], args.artist, args.cli))

    # starting the music
    input_listener.handler.play_pause()

    # waiting for media button input
    input_listener.startListening()