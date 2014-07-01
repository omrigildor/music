__author__ = 'omrigildor'

import socket
from globvars import host
from globvars import port
from globvars import bytes

# interprets the album list from the server
# returns the list of songs
def send_album(album_name, artist_id):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))

    print album_name
    s.send("-c " + album_name + "/" + artist_id)

    dat = s.recv(bytes)

    s.close()

    return dat


def send_song(song_name, rating, artist_id):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))

    s.send("-r " + song_name + "/" + rating + "/" + artist_id)

    dat = s.recv(bytes)
    s.close()

    return dat
