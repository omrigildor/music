import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import mclient as m
import client_rating as cr
from downloadthread import DownloadThread
from streamthread import StreamThread

class nSpotify(QWidget):
    
    artist_name = ""
    artist_id = 0
    album_name = ""
    album_list = []
    song_name = ""
    songs = []
    filepath = ""
    
    def __init__(self, parent=None):
        super(nSpotify, self).__init__(parent)
        self.list = QListWidget(self)
        self.line_edit = QLineEdit(self)
        self.line_edit.setText("Double click an artist")
        self.line_edit.setReadOnly(True)

        self.pbar = QProgressBar(self)
        self.start_over = QPushButton("Start Over")
        self.start_over.clicked.connect(self.start_again)
        self.stop = QPushButton("stop")
        self.start = QPushButton("start")
        self.pause = QPushButton("pause")

        self.grid = QGridLayout()
        hBox = QHBoxLayout()
        hBox.addWidget(self.pause)
        hBox.addWidget(self.start)
        hBox.addWidget(self.stop)
        self.grid.addWidget(self.line_edit, 0, 0)
        self.grid.addWidget(self.pbar, 1, 0)
        self.grid.addLayout(hBox, 2, 0)
        self.grid.addWidget(self.list, 3, 0)
        self.grid.addWidget(self.start_over, 4 , 0)

        self.setLayout(self.grid)
        self.setWindowTitle("NotSpotify")

        self.setGeometry(600, 300, 800, 600)

        self.get_artists()

    def start_again(self):
        self.list.itemClicked.disconnect(self.contextMenuEvent)
        self.pause.clicked.disconnect(self.workThreadS._pause)
        self.start.clicked.disconnect(self.workThreadS._power)
        self.stop.clicked.disconnect(self.workThreadS._stop)
        self.get_artists()

    
    def get_artists(self):
        artists = m.get_all()
        art_list = artists.split("+")
        self.list.clear()
        for x in art_list:
            x.split("/")
            self.list.addItem(x.split("/")[0])

        self.list.doubleClicked.connect(self.get_albums)


    def download(self):

        self.pbar.reset()
        self.pbar.setValue(0)
        print "Now in downloading"
        if self.filepath == "":
            text, ok = QInputDialog.getText(self, 'Filepath', 'Enter your filepath')
            if ok:
                text = unicode(text)
                self.filepath = text
                self.song_name = unicode(self.list.currentItem().text())
                self.workThread = DownloadThread(self.song_name, self.artist_id, text)
                self.connect(self.workThread, SIGNAL("Progress"), self.onProgress)
                self.workThread.start()
        else:
            self.song_name = unicode(self.list.currentItem().text())
            self.workThread = DownloadThread(self.song_name, self.artist_id, self.filepath)
            self.connect(self.workThread, SIGNAL("Progress"), self.onProgress)
            self.workThread.start()



    def rate(self):
        print "Now in rating"
        text, ok = QInputDialog.getText(self, 'Rating', 'Enter your rating (0 to 5)')
        if ok and float(text) <= 5 and float(text) >= 0:
            text = unicode(text)
            self.song_name = unicode(self.list.currentItem().text())
            update = cr.send_song(self.song_name, text, self.artist_id)
            self.line_edit.setText(update)
        
        else:
            self.box = QErrorMessage()
            self.box.setWindowTitle("Error")
            self.box.showMessage("Error: Rating must be 0 to 5")


    def onProgress(self):
        if self.pbar.value() >= 95:
            self.pbar.setValue(100)
            self.line_edit.setText("Finished")
            return
        self.pbar.setValue(self.pbar.value() + 5)


    def stream(self):

        text = unicode(self.list.currentItem().text())
        self.song_name = unicode(text)
        print "Now Streaming"
        self.workThreadS = StreamThread(self.song_name, self.artist_id)
        self.workThreadS.start()
        self.pause.clicked.connect(self.workThreadS._pause)

        self.start.clicked.connect(self.workThreadS._power)

        self.stop.clicked.connect(self.workThreadS._stop)



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



def main():
    app = QApplication(sys.argv)
    n = nSpotify()
    n.show()
    sys.exit(app.exec_())

