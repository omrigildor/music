__author__ = 'omrigildor'

import socket
import os
import sys
from globvars import host
from globvars import port
from globvars import operating_system
from globvars import bytes
import time
import moregui as mg
interval = 0

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


def stream_song(song_name, artist_id):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))
    from client_downloading import get_song_size
    f_size = int(get_song_size(song_name))
    s.send("-d " + song_name + "/" + artist_id)

    interval = f_size / 10
    size = 0
    song = 0
    if operating_system == "mac":
        import subprocess
        mp = open("/tmp/temp.mp3" , 'wb')
        while 1:
            dat = s.recv(bytes)
            if queue.get() == -1:
                break

            if not dat:
                p = subprocess.call(["afplay", mp.name])


            if (size > interval and song == 0):
                p = subprocess.call(["afplay", mp.name])
                size = 0
                mp.seek(0)



            if dat:
                mp.write(dat)
                size += bytes

            if (size > interval):
                song += 10
                queue.put(song)
                size = 0
                time.sleep(0)


        mp.close()
        p.kill()
        print "Thread is kill"
        if os.path.isfile("/tmp/temp.mp3"):
            os.remove("/tmp/temp.mp3")

        s.close()

    elif operating_system == "windows":

        import mp3play
        mp_dir = r"C:\WINDOWS\Temp\temp.mp3"
        mp = open(mp_dir , 'wb')


        while 1:


            if not dat:
                clip.play()
                break

            if (size > interval and song == 0):
                clip = mp3play.load(mp_dir)
                clip.play()
                size = 0
                mp.seek(0)
                song += 1

            if size > interval:
                song += 5
                interval = song
                size = 0


            if dat:
                mp.write(dat)


            size += bytes
            dat = s.recv(bytes)

        os.remove(mp)
        s.close()



def send_song(song_name, rating, artist_id):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))

    s.send("-r " + song_name + "/" + rating + "/" + artist_id)

    dat = s.recv(bytes)
    s.close()

    return dat
