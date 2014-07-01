__author__ = 'omrigildor'
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import socket
from globvars import *
import os


class StreamThread(QThread):
    stop = False
    pause = False
    power = False

    def __init__(self, song_name, artist_id):
        QThread.__init__(self)
        self.song_name = song_name
        self.artist_id = artist_id


    def __del__(self):
        self.wait()

    def _stop(self):
        os.system("killall afplay")
        self.stop = True

    def _pause(self):
        self.pause = True

    def power(self):
        self.power = True

    def run(self):
        from client_downloading import get_song_size
        f_size = get_song_size(self.song_name)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send("-d " + self.song_name + "/" + self.artist_id)
        interval = f_size / 10
        if operating_system == "mac":
            mp = open("/tmp/temp.mp3" , 'wb')
            import subprocess
            p = subprocess.Popen(["afplay", mp.name])
            while 1:
                if dat:
                    dat = s.recv(bytes)
                    mp.write(dat)

                if self.stop:
                    os.system("killall afplay")
                    break

                elif self.power:
                    p = subprocess.Popen(["afplay", mp.name])
                    self.power = False

                elif self.pause:
                    os.system("killall afplay")
                    self.pause = False

                elif p.pid == 0 and not self.power and not self.pause:
                    mp.seek(0)
                    p = subprocess.Popen(["afplay", mp.name])


            mp.close()
            os.system("killall afplay")
            if os.path.isfile("/tmp/temp.mp3"):
                os.remove("/tmp/temp.mp3")

            s.close()

        elif operating_system == "windows":
            import mp3play
            mp_dir = r"C:\WINDOWS\Temp\temp.mp3"
            mp = open(mp_dir , 'wb')

            while 1:
                if dat:
                    dat = s.recv(bytes)
                    mp.write(dat)

                if self.stop:
                    clip.stop()
                    break

                elif self.power:
                    clip.play()
                    self.power = False

                elif self.pause:
                    clip.pause()
                    self.pause = False

                elif not clip.isplaying() and not self.power and not self.pause:
                    clip = mp3play.load(mp_dir)
                    clip.play()
                    mp.seek(0)

            mp.close()
            clip.stop()
            if os.path.isfile(mp):
                os.remove(mp)

            s.close()