__author__ = 'omrigildor'
from PyQt4.QtCore import *
import socket
from globvars import *


class DownloadThread(QThread):
    def __init__(self, song_name, artist_id, filepath):
        QThread.__init__(self)
        self.song_name = song_name
        self.artist_id = artist_id
        self.filepath = filepath

    def __del__(self):
        self.wait()

    def run(self):
        from client_downloading import get_song_size
        f_size = get_song_size(self.song_name)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send("-d " + self.song_name + "/" + self.artist_id)
        mp = open(self.filepath + "/" + self.song_name, 'wb')

        interval = int(f_size) / 20
        size = 0
        dat = s.recv(bytes)
        while dat:
            if size >= interval:
                self.emit(SIGNAL("Progress"))
                size = 0

            size += bytes
            mp.write(dat)
            dat = s.recv(bytes)

        self.emit(SIGNAL("Progress"))
        mp.close()
        s.close()

