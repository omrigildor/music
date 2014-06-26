__author__ = 'omrigildor'

import socket
import tempfile
import os
from pygame import mixer
import sys
from globvars import host
from globvars import port
from globvars import operating_system
from globvars import bytes




# interprets the album list from the server
# returns the list of songs
def send_album(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))

    albums = data.split("+")

    count = 1
    for x in albums[:-1]:
        print str(count) + "-" +  x
        count += 1

    a_id = albums[-1]


    to_send = 0
    bl = False
    while not bl:
        try:
            to_send = int(
                raw_input("Which album would you like to search (enter a number)\n"))
            if to_send <= count - 1:
                bl = True
            else:
                print "Invalid Input"
        except ValueError:
            print "Invalid Input"

    s.send("-c " + albums[to_send - 1] + "/" + str(a_id))

    dat = s.recv(bytes)

    s.close()

    return dat, albums[to_send - 1]


def stream_song(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))

    songs = data.split("+")
    count = 1

    for x in songs[:-1]:
        print str(count) + "-" +  x
        count += 1

    a_id = songs[-1]

    to_send_song = 0
    bl = False
    while not bl:
        try:
            to_send_song = int(raw_input("What song would you like to stream? (enter a number)\n"))
            if to_send_song <= count - 1:
                bl = True
            else:
                print "Invalid Input"
        except ValueError:
            print "Invalid Input"

    s.send("-d " + songs[int(to_send_song) - 1] + "/" + a_id)


    dat = s.recv(bytes)

    count = 0
    song = 0

    size = 0


    if operating_system == "mac":
        import subprocess
        mp = open("/tmp/temp.mp3" , 'wb')
        while 1:

            if not dat:
                p = subprocess.call(["afplay", mp.name])
                break

            if (song > 400000 and count % 2 == 0):
                p = subprocess.call(["afplay", mp.name])
                song = 0
                mp.seek(0)

            if song > 200000:
                count += 1


            if dat:
                mp.write(dat)

            size += bytes
            song += bytes
            dat = s.recv(bytes)

        mp.close()
        if os.path.isfile("/tmp/temp.mp3"):
            os.remove("/tmp/temp.mp3")

        s.close()

    elif operating_system == "windows":

        import mp3play
        mp_dir = r"C:\WINDOWS\Temp\temp.mp3"
        mp = open(mp_dir , 'wb')
        import time


        while 1:


            if not dat:
                p = subprocess.call(["afplay", mp.name])
                break

            if (song > 400000 and count % 2 == 0):
                clip = mp3play.load(mp_dir)
                clip.play()
                mp.seek(0)
                count += 1


            if song > 200000:
                count += 1

            if dat:
                mp.write(dat)


            size += bytes
            song += bytes
            dat = s.recv(bytes)



        os.remove(mp)
        s.close()




def send_song(data):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))

    songs = data.split("+")
    count = 1

    for x in songs[:-1]:
        print str(count) + "-" +  x
        count += 1

    a_id = songs[-1]

    to_send_song = 0
    bl = False
    while not bl:
        try:
            to_send_song = int(raw_input("What song would you like to rate? (enter a number)\n"))
            if to_send_song <= count - 1:
                bl = True
            else:
                print "Invalid Input"
        except ValueError:
            print "Invalid Input"

    to_send_rating = -1
    bl = False
    while not bl:
        try:
            to_send_rating = float(raw_input("What rating? (0 to 5)\n"))
            if to_send_rating <= 5 and to_send_rating >= 0:
                bl = True
            else :
                print "Invalid Rating"
        except ValueError:
            print "Invalid input"



    s.send("-r " + songs[int(to_send_song) - 1] + "/" + str(to_send_rating) + "/" + a_id)

    dat = s.recv(bytes)
    s.close()

    print dat