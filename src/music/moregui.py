import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import mclient as m
import client_rating as cr
import threading
import thread
import client_downloading as cd

class nSpotify(QWidget):
    
    artist_name = ""
    artist_id = 0
    album_name = ""
    album_list = []
    song_name = ""
    songs = []
    
    def __init__(self, parent=None):
        super(nSpotify, self).__init__(parent)
        self.list = QListWidget(self)
        self.line_edit = QLineEdit("Double Click an artist to get started")
        self.line_edit.setReadOnly(True)
        self.get_artists()

        self.start_over = QPushButton("Start Over")
        self.start_over.clicked.connect(self.get_artists)

        vBox = QVBoxLayout()
        vBox.addWidget(self.line_edit)
        vBox.addWidget(self.list)
        vBox.addWidget(self.start_over)

        self.setLayout(vBox)
        self.setWindowTitle("NotSpotify")

        self.setGeometry(600, 300, 800, 600)

    def get_artists(self):
        artists = m.get_all()
        art_list = artists.split("+")
        self.list.clear()
        for x in art_list:
            x.split("/")
            self.list.addItem(x.split("/")[0])

        self.list.doubleClicked.connect(self.get_albums)

    def onProgress(self, val):
        self.pbar.setValue(val)
        if self.pbar.value() >= self.pbar.maximum():
            self.pbar.close()

    def download(self):
        self.pbar = QProgressDialog()
        print "Now in downloading"
        text, ok = QInputDialog.getText(self, 'Filepath', 'Enter your filepath')
        if ok:
            text = unicode(text)
            thread.start_new(cd.dl_song, (unicode(self.list.currentItem().text()), self.artist_id, text, True))

        return None

    def rate(self):
        print "Now in rating"

        text, ok = QInputDialog.getText(self, 'Rating', 'Enter your rating (0 to 5)')
        if ok and float(text) <= 5 and float(text) >= 0:
            text = unicode(text)
            self.song_name = unicode(self.list.currentItem().text())
            update = cr.send_song(self.song_name, text, self.artist_id)
            self.line_edit.setText(update)
        else:
            self.rate()

    def stream(self):
        self.pbar = QProgressDialog()
        self.pbar.setWindowTitle("Streaming")
        self.pbar.setRange(0, 100)
        self.pbar.show()

        text = unicode(self.list.currentItem().text())
        self.song_name = unicode(text)
        print "Now Streaming"
        self.thread = Worker()
        self.thread.song_name = self.song_name
        self.thread.artist_id = self.artist_id
        self.thread.run()
        if self.pbar.wasCanceled():
            self.thread.__del__()


    def get_albums(self):
        text = unicode(self.list.currentItem().text())
        print text, "artist chosen"
        print "Now in get_albums"
        album_list = m.send_artist(text)
        albums = album_list.split("+")
        count = 1

        self.list.clear()

        for x in albums[:-1]:
            self.list.addItem(x)
            count += 1

        self.artist_name = text
        self.artist_id = albums[-1]
        self.albums = albums[:-1]
        self.line_edit.setText("Double Click an Album")
        self.list.doubleClicked.disconnect(self.get_albums)
        self.list.doubleClicked.connect(self.get_songs)

    def contextMenuEvent(self, event):
        self.menu = QMenu(self)
        rate_act = QAction('Rate', self)
        rate_act.triggered.connect(self.rate)
        stream_act = QAction('Stream', self)
        stream_act.triggered.connect(self.stream)
        download_act = QAction('Download', self)
        download_act.triggered.connect(self.download)

        self.menu.addAction(rate_act)
        self.menu.addAction(stream_act)
        self.menu.addAction(download_act)
        self.menu.popup(QCursor.pos())

    def get_songs(self):
        self.line_edit.setText("Right click a song")

        text = unicode(self.list.currentItem().text())
        print "Now in get_songs"
        self.album_name = text

        song_list = cr.send_album(self.album_name, self.artist_id)

        songs = song_list.split("+")
        count = 1
        self.list.clear()
        for x in songs[:-1]:
            self.list.addItem(x)
            count += 1

        self.songs = songs[:-1]

        self.list.doubleClicked.disconnect(self.get_songs)

        self.list.itemClicked.connect(self.contextMenuEvent)

class Worker(QThread):
    song_name = ""
    artist_id = ""

    def __init__(self, parent = None):
        super(Worker, self).__init__(parent)
        self.exiting = False

    def __del__(self):
        self.exiting = True
        self.wait()

    def render(self):
        self.exiting = False
        self.start()

    def run(self):
        while not self.exiting:
            cr.stream_song(self.song_name, self.artist_id)


def main():
    app = QApplication(sys.argv)
    n = nSpotify()
    n.show()
    sys.exit(app.exec_())

