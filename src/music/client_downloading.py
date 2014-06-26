__author__ = 'omrigildor'

import socket
import time
import sys
import datetime
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

    FMT = '%H:%M:%S'

    s1 = time.strftime("%H:%M:%S", time.localtime())

    sys.stdout.write("Loading [")
    sys.stdout.flush()
    for x in albums[:-1]:

        y = dl_artist_helper(x, a_id)
        dl_album(y, filepath + "/" + artist_name, x)
        sys.stdout.write('\b000')
        sys.stdout.flush()

    s2 = time.strftime("%H:%M:%S", time.localtime())
    print s2
    tdelta = datetime.datetime.strptime(s2, FMT) - datetime.datetime.strptime(s1, FMT)

    print "Time to download artist ", tdelta




def dl_album(data, filepath, name):

    os.mkdir(filepath + "/" + name)

    songs = data.split("+")
    a_id = songs[-1]

    FMT = '%H:%M:%S'

    s1 = time.strftime("%H:%M:%S", time.localtime())

    for x in songs[:-1]:
        sys.stdout.write("\b.")
        dl_song(x, a_id, filepath + "/" + name)

    s2 = time.strftime("%H:%M:%S", time.localtime())
    print s2
    tdelta = datetime.datetime.strptime(s2, FMT) - datetime.datetime.strptime(s1, FMT)

    print "Time to download album ", tdelta

def get_song(data, filepath):

    songs = data.split("+")
    count = 1


    for x in songs[:-2]:
        print str(count) + "-" +  x
        count += 1

    a_id = songs[-1]
    to_send_song = 0
    bl = False
    while not bl:
        try:
            to_send_song = int(raw_input("What song would you like to download? (enter a number)\n"))
            if to_send_song <= count - 1:
                bl = True
            else:
                print "Invalid Input"
        except ValueError:
            print "Invalid Input"

    dl_song(songs[int(to_send_song) - 1], a_id, filepath)




def dl_song(song_name, a_id, filepath):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))

    s.send("-d " + song_name + "/" + a_id)

    dat = s.recv(bytes)
    mp = open(filepath + "/" + song_name, 'wb')

    FMT = '%H:%M:%S'

    s1 = time.strftime("%H:%M:%S", time.localtime())

    i = 0.0
    size = 0.0
    sys.stdout.flush()
    while dat:
        if (i%4) == 0:
            sys.stdout.write('\b/')
        elif (i%4) == 1:
            sys.stdout.write('\b-')
        elif (i%4) == 2:
            sys.stdout.write('\b\\')
        elif (i%4) == 3:
            sys.stdout.write('\b|')


        i += .1
        mp.write(dat)
        dat = s.recv(bytes)
        size += bytes

    mp.close()
    s2 = time.strftime("%H:%M:%S", time.localtime())
    tdelta = datetime.datetime.strptime(s2, FMT) - datetime.datetime.strptime(s1, FMT)

    print "Time to Download ", tdelta, " Filesize ", size

    s.close()