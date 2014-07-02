__author__ = 'omrigildor'

import socket
import os
from globvars import port
from globvars import host
from globvars import bytes

def dl_artist_helper(album_name, a_id):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))

    s.send("-c " + album_name + "/" + str(a_id))

    dat = s.recv(bytes)

    s.close()

    return dat


def dl_artist(data, filepath, artist_name):

    albums = data.split("+")
    a_id = albums[-1]

    if not os.path.isdir(filepath + "/" + artist_name):
        os.mkdir(filepath + "/" + artist_name)


    for x in albums[:-1]:
        y = dl_artist_helper(x, a_id)
        dl_album(y, filepath + "/" + artist_name, x)


def dl_album(data, filepath, name):

    os.mkdir(filepath + "/" + name)

    songs = data.split("+")
    a_id = songs[-1]

    for x in songs[:-1]:
        dl_song(x, a_id, filepath + "/" + name)



def get_song_size(song_name):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send("-gi %s" % song_name)
    dat = s.recv(bytes)
    s.close()
    return dat


def dl_song(song_name, a_id, filepath):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))

    s.send("-d " + song_name + "/" + a_id)

    mp = open(filepath + "/" + song_name, 'wb')


    dat = s.recv(bytes)
    while dat:

        mp.write(dat)
        dat = s.recv(bytes)

    mp.close()
    s.close()

