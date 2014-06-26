import socket
import sys
import os
import client_rating as cr
import client_downloading as cd
from pygame import mixer
from globvars import host
from globvars import port
from globvars import bytes

operating_system = "mac"

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
def send_artist():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((host, port))

    except:
        print "Could not connect"
        sys.exit()

    artist = raw_input("Choose an artist\n")
    to_send = "-a " + artist
    try:
        s.send(to_send)

    except:
        print "Could not connect"
        sys.exit()
    data = s.recv(bytes)
    s.close()
    return data, artist



choice = raw_input("Would you like to stream, rate or download or play a song? (rate or download)\n")

if choice == "rate":
    print "rating"
    x = send_artist()

    y = cr.send_album(x[0])

    cr.send_song(y[0])

elif choice == "play":
    play_song()

elif choice == "stream":
    x = send_artist()
    y = cr.send_album(x[0])
    cr.stream_song(y[0])


elif choice == "download":
    print "downloading"
    x = send_artist()
    ans = raw_input("Would you like to download all albums?\n")

    if ans == "yes":
        ans = raw_input("Enter your filepath\n")
        cd.dl_artist(x[0], ans, x[1])

    else:
        y = cr.send_album(x[0])
        data = y[0]
        album_name = y[1]

        ans = raw_input("Would you like to download all songs?\n")
        if ans == "yes":
            ans = raw_input("Enter your filepath\n")
            cd.dl_album(data, ans, album_name)

        else:
            ans = raw_input("Enter your filepath\n")
            cd.get_song(data, ans)



