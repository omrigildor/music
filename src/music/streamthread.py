__author__ = 'omrigildor'
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import socket
from globvars import *
import os


class StreamThread(QThread):
    stop = False
    pause = False

    def __init__(self, song_name, artist_id):
        QThread.__init__(self)
        self.song_name = song_name
        self.artist_id = artist_id
        self.connect(self, SIGNAL("Stop"), self._stop)
        self.connect(self, SIGNAL("Pause"), self._pause)
        self.connect(self, SIGNAL("Start"), self._start)


    def __del__(self):
        self.wait()

    def _stop(self):
        self.stop = True

    def _pause(self):
        self.pause = True

    def _start(self):
        self.pause = False

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
            size = 0
            song = 0
            while 1:
                if self.stop:
                    os.system("killall afplay")
                    break

                if self.pause:
                    os.system("killall afplay")

                else:
                    dat = s.recv(bytes)
                    mp.write(dat)
                    size += bytes
                    if dat:
                        mp.write(dat)

                    if not dat:
                        p = subprocess.Popen(["afplay", mp.name]).pid
                        break

                    if size >= interval and song == 0:
                        p = subprocess.Popen(["afplay", mp.name]).pid
                        size = 0
                        mp.seek(0)

                    if song == 2 and p != 0:
                        p = subprocess.Popen(["afplay", mp.name])

            mp.close()
            p.kill()
            if os.path.isfile("/tmp/temp.mp3"):
                os.remove("/tmp/temp.mp3")

            s.close()
