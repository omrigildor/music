import subprocess
from PyQt4.QtGui import *
import twistedclient as tc
from globtwisted import *
import os

class nSpotify(QWidget):

    pid = 0
    artist_name = ""
    artist_list = []
    artist_id = 0
    album_name = ""
    album_list = []
    song_name = ""
    songs = []
    song_data = ""
    filepath = ""
    filesize = 0
    streaming = False
    
    def __init__(self, reactor, parent=None):
        super(nSpotify, self).__init__(parent)
        self.reactor = reactor
        self.list = QListWidget(self)
        self.line_edit = QLineEdit(self)
        self.line_edit.setText("Double click an artist")
        self.line_edit.setReadOnly(True)
        self.set_factory()
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

    #creates the gui's factory
    def set_factory(self):
        self.factory = tc.mClientFactory(self)
        self.connection = self.reactor.connectTCP(host, port, self.factory)

    # sets the self.client to the twisted client
    def set_client(self, client):
        self.client = client

    # button to reset the client after rating/streaming/downloading a song
    def start_again(self):
        try:
            self.list.itemClicked.disconnect(self.contextMenuEvent)
        except:
            print "OK"
        try:
            self.pause.clicked.disconnect(self.workThreadS._pause)
            self.start.clicked.disconnect(self.workThreadS._power)
            self.stop.clicked.disconnect(self.workThreadS._stop)
        except:
            print "yah"
        self.list_artists("+".join(self.artist_list))

    # takes the string of artists and displays them in the self.list
    def list_artists(self, artists):
        art_list = artists.split("+")
        self.artist_list = art_list
        self.list.clear()
        for x in art_list:
            x.split("/")
            self.list.addItem(x.split("/")[0])

        self.list.doubleClicked.connect(self.get_artist)

    #updates the line_edit text
    def update_text(self, txt):
        self.line_edit.setText(txt)

    #sets the filesize of the chosen song
    def set_filesize(self, i):
        print "filesize updated to", i
        self.filesize = i

    def download_finish(self):
        print "download finished"
        self.fille.close()
        if self.streaming:
            self.filepath = ""
            self.song_name = ""
        self.streaming = False

    def download_test(self, data):
        self.fille.write(data)
        self.filesize += len(data)
        if self.streaming and self.pid == 0 and operating_system == "mac" and self.filesize >= self.interval:
            p = subprocess.Popen(["afplay", "/tmp/temp.mp3"])
            self.pid = p.pid
            self.fille.seek(0)

        if self.filesize >= self.interval:
            self.onProgress()
            self.filesize = 0



    # downloads a file
    def download(self):
        self.song_name = str(self.list.currentItem().text())
        self.client.get_song_size(self.song_name)
        self.interval = self.filesize / 20
        self.pbar.reset()
        self.pbar.setValue(0)
        print "Now in downloading"
        if self.filepath == "":
            text, ok = QInputDialog.getText(self, 'Filepath', 'Enter your filepath')
            if ok:
                self.filepath = text
                self.fille = open(self.filepath + "/" + self.song_name, "wb")
                self.filesize = 0
                self.client.download_song(self.song_name, self.artist_id)
        else:
            self.fille = open(self.filepath + "/" + self.song_name, "wb")
            self.filesize = 0
            self.client.download_song(self.song_name, self.artist_id)

    # rates a song showing a dialog box
    def rate(self):
        print "Now in rating"
        text, ok = QInputDialog.getText(self, 'Rating', 'Enter your rating (0 to 5)')
        if ok and float(text) <= 5 and float(text) >= 0:
            self.song_name = str(self.list.currentItem().text())
            self.client.send_rating(self.song_name, str(text), self.artist_id)
        
        else:
            self.box = QErrorMessage()
            self.box.setWindowTitle("Error")
            self.box.showMessage("Error: Rating must be 0 to 5")

    # updates the progress bar
    def onProgress(self):
        if self.pbar.value() >= 95:
            self.pbar.setValue(100)
            self.line_edit.setText("Finished")
            return
        self.pbar.setValue(self.pbar.value() + 5)

    # streams a song
    def stream(self):
        text = str(self.list.currentItem().text())
        self.song_name = "temp.mp3"
        print "Now Streaming"
        self.filepath = "/tmp"
        self.client.get_song_size(text)
        self.interval = self.filesize / 20
        self.fille = open(self.filepath + "/" + self.song_name, "wb")
        self.streaming = True
        self.filesize = 0
        self.client.download_song(text, self.artist_id)
        if operating_system == "mac":
            self.stop.clicked.connect(self.stop_song)
            self.pause.clicked.connect(self.pause_song)
            self.start.clicked.connect(self.start_song)

    def pause_song(self):
        subprocess.Popen(["killall", "afplay"])
        print "stopping song"

    def start_song(self):
        subprocess.Popen(["afplay", "/tmp/temp.mp3"])
        print "playing song"

    def stop_song(self):
        subprocess.Popen(["killall", "afplay"])
        os.remove("/tmp/temp.mp3")

    # takes the chosen artist and sends it to the server
    def get_artist(self):
        text = str(self.list.currentItem().text())
        print text, "artist chosen"
        self.artist_name = text
        self.client.send_artist(text)

    # list the albums for an artist
    def list_albums(self, line):
        print "called list albums"
        albums = line.split("+")
        count = 1

        self.list.clear()

        for x in albums[:-1]:
            self.list.addItem(x)
            count += 1

        self.artist_id = albums[-1]
        self.albums = albums[:-1]
        self.line_edit.setText("Double Click an Album")
        self.list.doubleClicked.disconnect(self.get_artist)
        self.list.doubleClicked.connect(self.get_songs)

    # context menu
    # sets it up so a click allows user to rate/stream/download
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

    # takes the chosen album and sends it to the server
    def get_songs(self):
        self.line_edit.setText("Right click a song")
        text = str(self.list.currentItem().text())
        print "Now in get_songs"
        self.album_name = text
        self.client.send_album(self.album_name, self.artist_id)

    # lists the songs for an album in self.list
    def list_songs(self, line):
        print "list_songs called"
        songs = line.split("+")
        count = 1
        self.list.clear()
        for x in songs[:-1]:
            self.list.addItem(x)
            count += 1

        self.songs = songs[:-1]
        self.list.doubleClicked.disconnect(self.get_songs)
        self.list.itemClicked.connect(self.contextMenuEvent)
