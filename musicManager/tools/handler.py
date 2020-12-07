import eyed3

from os import path
from random import shuffle
from urllib.parse import unquote_plus, urlparse
from vlc import Instance, EventType, PlaybackMode

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
        print(f'''
playing {file}:
    artist:  {fileInfo["artist"]}
    title:   {fileInfo["title"]}
    album:   {fileInfo["album"]}
    genre:   {fileInfo["genre"]}''')

    def play_pause(self):
        if self.playing:
            collector.stop_playlist_timer()
            collector.stop_song_timer()
            self.playlistPlayer.pause()
        else:
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