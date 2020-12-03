# musicManager  
##### A python3 command-line music player,  
##### automatically adds all directories (with mp3 files) in your Music directory _($home/Music)_ as playlists

## Installation
```shell script
git clone https://github.com/dadope/musicManager  # clone (download) the repository
cd musicManager                                   # enter the project directory
make install                                      # installation, alternatively use pip(3) install .
```
## Usage
```
usage: musicManager [-h] [-p PLAYLIST] [-a ARTIST] [-n] [-c] [-r]

plays music

optional arguments:
  -h, --help            show this help message and exit
  -p PLAYLIST, --playlist PLAYLIST
                        Specify the playlist to play
  -a ARTIST, --artist ARTIST
                        Specify the artist to play
  -n, --alphabet        play in alphabetic order
  -c, --cli             display cli information
  -r, --random          play randomly
```
