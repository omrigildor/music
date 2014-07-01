import socket
import sys
import os
from pygame import mixer
from globvars import host
from globvars import port
from globvars import bytes

def get_all():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send("-all ")
    dat =  s.recv(bytes)
    s.close()
    return dat

def play_song():

    cwd = os.path.abspath(raw_input("Enter your filepath\n"))

    all_songs = dict()
    count = 1
    for root, _, files in os.walk(cwd):
        for f in files:
            fullpath = os.path.join(root, f)
            if f.endswith("mp3"):
                print str(count) + "-" + f
                all_songs[str(count)] = fullpath
                count += 1

    ans = raw_input("Pick a number of a song\n")

    song_name = all_songs[ans].split("/")[-1]
    song_path = all_songs[ans].split(song_name)[0]

    print "Now playing: ", all_songs[ans].split("/")[-1]
    os.chdir(os.path.abspath(song_path))
    mixer.init()
    mixer.music.load(song_name)

    while 1:
        ans = raw_input("p for pause, r to resume, s to stop, n to play song, q to quit\n")

        if ans == "p":
            mixer.music.pause()

        elif ans == "r":
            mixer.music.unpause()

        elif ans == "s":
            mixer.music.stop()

        elif ans == "n":
            mixer.music.play()

        elif ans == "q":
            break



# This sends an artist to the server
# receives the list of albums back in a string
def send_artist(artist_name):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
    except:
        print "Could not connect"
        sys.exit()
    to_send = "-a " + artist_name
    try:
        s.send(to_send)
    except:
        print "Could not connect"
        sys.exit()
    data = s.recv(bytes)
    s.close()
    return data

