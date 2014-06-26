import os
import sys
from mutagen.mp3 import MP3
from optparse import OptionParser
from library import Library
from song import Song
import pymysql



# get_library : path -> library
def get_library(loc):
    os.chdir(os.path.abspath(loc))
    path = os.path.abspath(loc)
    res = Library(path, [], [], [], [])

    for mp in os.listdir(path):
        lst = []
        if os.path.isdir(mp):
            artist = mp.split("-")[0]
            for i in os.listdir(mp):
                if i.split(".")[-1] == "mp3":
                    song = i
                    size = os.path.getsize(path + "/" + mp + "/" + i)
                    duration = MP3(path + "/" + mp + "/" + i).info.length
                    new_song = Song(song, artist, i, duration, size)
                    res.add_song(new_song)
                    lst.append(new_song)
            res.add_artist(len(lst), artist)

        elif mp.split(".")[-1] == "mp3":

            name = mp.split("-")[1]
            artist = mp.split("-")[0]
            size = os.path.getsize(path + "/" + mp)
            duration = MP3(path + "/" + mp).info.length
            new_song = Song(name, artist, "single", duration, size)
            res.add_song(new_song)
            res.add_artist(1, mp)

    return res


def size(music):
    music.sort_biggest()


def duration(music):
    music.sort_longest()


def artists(music):
    music.sort_artist()


def lst(my_music):
    print "-size\n-length\n-artist\n-list"


def main(argv):

    my_music = get_library("/Users/omrigildor/Downloads/Music")

    parser = OptionParser()

    # parser.add_argument("--path", action = "store",
    # dest = "get_library", help = "path name")

    parser.add_option("-l", "--length" , action = "store_true",
                      dest = "d",  help = "longest song")

    parser.add_option("-s", "--size", action = "store_true",
                      dest = "s" , help = "biggest song")

    parser.add_option("-a", "--artist", action = "store_true",
                      dest = "a", help = "number 1 artist")

    parser.add_option("-o", "--search", dest = "let", type = "str", help = "search for letter")

    options = parser.parse_args()

    if len(sys.argv) > 1:
        my_music.get_letter(options[0].let)

    if options[0].d:
        duration(my_music)

    if options[0].s:
        size(my_music)

    if options[0].a:
        artists(my_music)

main(sys.argv[1])


