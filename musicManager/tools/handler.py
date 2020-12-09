from time import sleep

import eyed3

from os import path
from random import shuffle
from urllib.parse import unquote_plus, urlparse
from vlc import Instance, EventType, PlaybackMode

from ..tools import cli
from ..constants import collector

# playlist sort
RANDOM_ORDER = "random"
ALPHABETIC_ORDER = "alphabet"

class mediaHandler:
    def __init__(self, songs:list, playlist:dict, orderToPlay:str=None, artist:str=None, cli:bool=True):
        """
        handles everything related to playing the music

        :param songs: list of mp3 files to play
        :param orderToPlay: defines the order in which the files are played, can be either "random", "alphabet" or None
        :param cli: defines if anything is printed to the screen
        """

        self.cli = cli
        self.songs = songs
        self.artist = artist
        self.orderToPlay = orderToPlay
        self.playlist_name = playlist["playlist"]
        self.vlc_instance = Instance()

        self.playing = False
        self.curr_media_player = None

        # length of the song
        self.curr_song_max_seconds = 0

        # seconds that the song has been playing
        self.curr_song_playing_seconds = 0

        # percentage of the song already played
        self.curr_song_percentage = 0


        if self.artist:
            self.songs = [x for x in self.songs if self.getFileInfo(x)["artist"].lower() == self.artist.lower()]

            if len(self.songs) < 1:
                print("Artist could not be found in the playlist, exiting")
                collector.log_critical_and_exit(f"Could not find artist {self.artist}", 1)

        if orderToPlay == RANDOM_ORDER:
            if self.cli: print("Randomly sorting the playlist...")
            shuffle(self.songs)

        elif orderToPlay == ALPHABETIC_ORDER:
            if self.cli: print("Alphabetically sorting the playlist...")
            self.songs = sorted(self.songs, key=str.lower)

        # confirming that there are songs to be played
        if len(songs) == 0:
            print("There are no songs to be played, exiting")
            collector.log_critical_and_exit("no songs to be played", 1)

        self.currFile = self.songs[0]
        self.currFilename = path.basename(self.currFile)

        self.playlistPlayer = self.vlc_instance.media_list_player_new()

        # lets the player loop
        self.playlistPlayer.set_playback_mode(PlaybackMode.loop)

        # creates a new media list with all the songs in the playlist
        self.playlist = self.vlc_instance.media_list_new(self.songs)

        # adds the created playlist to playlistPlayer
        self.playlistPlayer.set_media_list(self.playlist)

        # function gets called on every playback event
        #
        # gets the base filename of the audio file currently playing
        # if commandline-mode enabled: then prints information out about the file
        def listPlayerCallback(event):
            self.currFile = self.getFilename(self.playlistPlayer.get_media_player().get_media().get_mrl())
            self.currFilename = path.basename(self.currFile)

            if self.cli:
                self.printFileInfo(self.getFileInfo(self.currFile), self.currFile)

        self.list_player_events = self.playlistPlayer.event_manager()
        self.list_player_events.event_attach(EventType.MediaListPlayerNextItemSet, listPlayerCallback)

    # callback for MediaPlayerTimeChanged, gets the percentage, and time played of the current song and calls printProgressBar
    def _media_player_callback(self, event):

        # for unknown reasons self.curr_media_player.get_length() returns -1 in _set_event_callback_for_current_file
        if self.curr_song_max_seconds == -1:
            self.curr_song_max_seconds = self.curr_media_player.get_length()/1000

        #self.curr_song_percentage = self.curr_media_player.get_position()

        _current_percentage = self.curr_media_player.get_position()*100
        self.curr_song_percentage = float('{:.2f}'.format(round(_current_percentage, 2)))
        self.curr_song_playing_seconds = self.curr_media_player.get_time()/1000

        cli.printProgressBar(self.curr_song_percentage, prefix=cli.format_time(self.curr_song_max_seconds, self.curr_song_playing_seconds))

    # gets called when
    def _set_event_callback_for_current_file(self):
        self.curr_media_player = self.playlistPlayer.get_media_player()
        self.curr_media_player_events = self.curr_media_player.event_manager()
        self.curr_media_player_events.event_attach(EventType.MediaPlayerTimeChanged, self._media_player_callback)

        self.curr_song_max_seconds = self.curr_media_player.get_length()

    # cleanup before going to the next song
    def _remove_event_callback_for_current_file(self):
        self.curr_media_player_events.event_detach(EventType.MediaPlayerTimeChanged)
        self.curr_media_player_events = None
        self.curr_media_player = None


    # finds out information about the given file through metadata
    def getFileInfo(self, file:str) -> dict:
        audiofile = eyed3.load(file)

        album = audiofile.tag.album
        genre = audiofile.tag.genre
        title = audiofile.tag.title
        artist = audiofile.tag.artist

        return {
            "artist": artist,
            "title": title,
            "album":album,
            "genre":genre
        }

    # prints out information about a file (used in conjunction with getFileInfo)
    def printFileInfo(self, fileInfo, file):
        print(f'''\n\nplaying {file}:
    artist:  {fileInfo["artist"]}
    title:   {fileInfo["title"]}
    album:   {fileInfo["album"]}
    genre:   {fileInfo["genre"]}\n''')

    def play_pause(self):
        if self.playing:
            self._remove_event_callback_for_current_file()

            collector.stop_playlist_timer()
            collector.stop_song_timer()
            self.playlistPlayer.pause()
        else:
            self._set_event_callback_for_current_file()

            collector.start_playlist_timer(self.playlist_name)
            collector.start_song_timer(self.currFile)
            self.playlistPlayer.play()

        self.playing = not self.playing

    def next(self):
        # usable because if no song is playing the function just returns without any effects
        collector.stop_song_timer()

        self.playlistPlayer.next()
        collector.start_song_timer(self.currFile)

    def previous(self):
        # usable because if no song is playing the function just returns without any effects
        collector.stop_song_timer()

        self.playlistPlayer.previous()
        collector.start_song_timer(self.currFile)

    def getFilename(self, uri):
        return unquote_plus(urlparse(uri).path)