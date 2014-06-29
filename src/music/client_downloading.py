__author__ = 'omrigildor'

import socket
import time
import sys
import datetime
import os
import progressbar
from globvars import port
from globvars import host
from globvars import bytes
from progressbar import ProgressBar
from nItunes import cur



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

    pb = ProgressBar()
    pb.start()
    interval = albums[:-1] / 100
    i = 0

    for x in albums[:-1]:
        pb.update(i)
        i += interval
        y = dl_artist_helper(x, a_id)
        dl_album(y, filepath + "/" + artist_name, x)

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

    pb = ProgressBar()
    pb.start()

    interval = songs[:-1] / 100
    i = 0

    for x in songs[:-1]:
        pb.update(i)
        i += interval
        dl_song(x, a_id, filepath + "/" + name, False)

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

    dl_song(songs[int(to_send_song) - 1], a_id, filepath, True)


def get_song_size(song_name):
    cur.execute("SELECT size from songs where name = '%s'" % song_name)
    f_size = str(cur.fetchone()[0])

    return f_size

def dl_song(song_name, a_id, filepath, bl):

    f_size = get_song_size(song_name)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))

    s.send("-d " + song_name + "/" + a_id)

    dat = s.recv(bytes)
    mp = open(filepath + "/" + song_name, 'wb')

    FMT = '%H:%M:%S'



    s1 = time.strftime("%H:%M:%S", time.localtime())

    interval = int(f_size) / 20

    size = 0
    count = 0
    if bl:
        pb = ProgressBar()
        pb.start()

    while dat:
        if size > interval and bl:
            count += 5
            pb.update(count)
            size = 0

        size += bytes
        mp.write(dat)
        dat = s.recv(bytes)

    pb.finish()
    mp.close()
    s2 = time.strftime("%H:%M:%S", time.localtime())
    tdelta = datetime.datetime.strptime(s2, FMT) - datetime.datetime.strptime(s1, FMT)

    print "Time to Download ", tdelta, " Filesize ", size

    s.close()


