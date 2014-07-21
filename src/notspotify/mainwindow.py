from __future__ import print_function
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import twistedclient as tc
from constants import *
import os
from pydub import AudioSegment
from streamthread import StreamThread
import pyaudio

class nSpotify(QWidget):

    artist_name = ""
    artist_list = []
    artist_id = 0
    album_name = ""
    album_list = []
    song_name = ""
    songs = []
    song_data = ""
    # from the server the path of the original file
    filepath = ""
    # what the path of the song downloading will be
    song_path = ""
    filesize = 0
    width = 8
    chan = 2
    frate = 44100
    length = 0
    mark = 0
    streaming = False
    bytelist = []
    skipped = 0

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
        self.sld = QSlider(Qt.Horizontal, self)

        self.grid = QGridLayout()
        hBox = QHBoxLayout()
        hBox.addWidget(self.pause)
        hBox.addWidget(self.start)
        hBox.addWidget(self.stop)
        self.grid.addWidget(self.line_edit, 0, 0)
        self.grid.addWidget(self.sld, 1, 0)
        self.grid.addWidget(self.pbar, 2, 0)
        self.grid.addLayout(hBox, 3, 0)
        self.grid.addWidget(self.list, 4, 0)
        self.grid.addWidget(self.start_over, 5 , 0)

        self.setLayout(self.grid)
        self.setWindowTitle("NotSpotify")

        self.setGeometry(600, 300, 800, 600)

    #creates the gui's factory
    def changeValue(self):
        self.skipped = 0
        print ("Slider")
        self.workThread.end()
        self.client.stream = False
        self.bytelist = []
        value = self.sld.value()
        perc = (value / 100.0) * self.length
        perc = int(perc)
        self.skipped = perc
        while perc % 2 != 0:
            perc = perc - 1
        print(perc, "Value skipping to")

        self.stream_song(perc)

    def sld_value(self):
        self.sld.setValue(self.sld.value() + 1)

    def clear_all(self):
        self.artist_name = ""
        self.artist_id = 0
        self.album_name = ""
        self.album_list = []
        self.song_name = ""
        self.songs = []
        self.song_data = ""
        # from the server the path of the original file
        self.filepath = ""
        # what the path of the song downloading will be
        self.song_path = ""
        self.filesize = 0
        self.width = 8
        self.chan = 2
        self.frate = 44100
        self.length = 0
        self.mark = 0
        self.streaming = False
        self.bytelist = []
        self.skipped = 0

    def set_factory(self):
        self.factory = tc.mClientFactory(self)
        self.connection = self.reactor.connectTCP(host, port, self.factory)

    # sets the self.client to the twisted client
    def set_client(self, client):
        self.client = client

    # button to reset the client after rating/streaming/downloading a song
    def start_again(self):
        self.client.stream = False
        self.client.down = False
        self.client.begin = True
        try:
            self.workThread.end()
            self.client.stream = False
            self.menu.clear()
            self.menu.popup.disconnect()
            self.list.itemClicked.disconnect(self.contextMenuEvent)
            self.sld.releaseMouse.disconnect()
            self.list.itemClicked.disconnect()
            self.list.clicked.disconnect()
        except:
            print("ERROR")
        try:
            self.list.doubleClicked.disconnect()
            self.pause.clicked.disconnect()
            self.start.clicked.disconnect()
            self.stop.clicked.disconnect()
        except:
            print("ERROR 2")


        try:
            self.list.itemClicked.disconnect(self.contextMenuEvent)
        except:
            pass

        print("Starting_Over")
        self.client.get_all()

    # takes the string of artists and displays them in the self.list
    def list_artists(self, artists):
        art_list = artists.split("+")
        self.artist_list = art_list
        self.list.clear()
        for x in art_list:
            if x.split("/")[0] != "":
                self.list.addItem(x.split("/")[0])

        self.list.doubleClicked.connect(self.get_artist)
        print("List artists")

    #updates the line_edit text
    def update_text(self, txt):
        self.line_edit.setText(txt)

    #sets the filesize of the chosen song
    def set_filesize(self, i):
        print ("filesize updated to", i)
        self.filesize = i

    def set_info(self, width, chan, frate, length):
        print ("Setting information")
        self.width = int(width)
        self.chan = int(chan)
        self.frate = int(frate)
        self.length = int(length)

    def download_finish(self):
        print ("download finished")
        self.fille.close()
        AudioSegment.from_wav(str(self.song_path) + ".wav").export(str(self.song_path) + ".mp3", format="mp3")
        os.remove(self.song_path + ".wav")
        self.line_edit.setText("Finished Downloading File")

    def set_position(self):
        print("Position Set")
        self.mark = self.skipped + self.workThread.position
        if self.mark % 2 != 0:
            self.mark -= 1
        print(self.mark)


    def play_stream(self):
        if not self.streaming:
            self.workThread.start()
            self.streaming = True

    def download_test(self, data):
        self.filesize += len(data)
        self.fille.write(data)
        if self.filesize >= self.interval:
            self.onProgress()
            self.filesize = 0


    # downloads a file
    def download(self):
        self.song_name = str(self.list.currentItem().text())
        print (self.song_name)
        self.client.get_song_size(self.song_name)
        self.interval = self.filesize / 20
        self.pbar.reset()
        self.pbar.setValue(0)
        print ("Now in downloading")
        if self.filepath == "":
            text, ok = QInputDialog.getText(self, 'Filepath', 'Enter your filepath')
            if ok:
                self.filepath = text
                self.song_path = self.filepath + "/" + self.song_name.split(".mp3")[0]
                self.fille = open(self.song_path + ".wav", "wb")
                self.filesize = 0
                self.client.download_song(self.song_name, self.artist_id)
        else:
            self.song_path = self.filepath + "/" + self.song_name.split(".mp3")[0]
            self.fille = open(self.song_path + ".wav", "wb")
            self.filesize = 0
            self.client.download_song(self.song_name, self.artist_id)


    # rates a song showing a dialog box
    def rate(self):
        print ("Now in rating")
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
        try:
            self.workThread.end()
            self.client.stream = False
            self.bytelist = []
            self.sld.setValue(0)
        except:
            print("No Song started yet")
        self.update_text("Streaming!               :)")
        text = str(self.list.currentItem().text())
        self.song_name = text
        self.client.get_info(text, self.artist_id)
        print ("Now Streaming")
        self.client.get_song_size(text)
        self.interval = self.filesize / 20
        self.stop.clicked.connect(self.stop_song)
        self.pause.clicked.connect(self.pause_song)
        self.start.clicked.connect(self.start_song)
        self.sld.sliderReleased.connect(self.changeValue)
        self.stream_song(0)

    def stream_song(self, index):
        print("Start Stream")
        self.bytelist = []
        self.streaming = False
        self.p = pyaudio.PyAudio()
        self.streamer = self.p.open(format = self.width, channels = self.chan, rate = self.frate, output = True)
        second = self.length * .01
        self.workThread = StreamThread(self.bytelist, self.streamer, self.p, second)
        self.connect(self.workThread, SIGNAL("Pause"), self.set_position)
        self.connect(self.workThread, SIGNAL("Tick"), self.sld_value)
        self.client.set_thread(self.workThread)
        self.client.stream_song(self.song_name, self.artist_id, index)

    def pause_song(self):
        print("Paused")
        self.workThread.end()
        self.client.stream = False
        self.bytelist = []

    def start_song(self):
        print ("Started")
        self.workThread.end()
        self.client.stream = False
        self.stream_song(self.mark)

    def stop_song(self):
        self.workThread.end()
        self.client.stream = False
        self.bytelist = []
        self.mark = 0
        self.skipped = 0
        self.length = 0
        print ("stopped")

    # takes the chosen artist and sends it to the server
    def get_artist(self):
        text = str(self.list.currentItem().text())
        print (text, "artist chosen")
        self.artist_name = text
        self.client.send_artist(text)

    # list the albums for an artist
    def list_albums(self, line):
        print ("called list albums")
        albums = line.split("+")
        count = 1

        self.list.clear()

        for x in albums[:-1]:
            self.list.addItem(x)
            count += 1

        self.artist_id = albums[-1]
        self.albums = albums[:-1]
        self.line_edit.setText("Double Click an Album")
        self.list.doubleClicked.disconnect()
        self.list.doubleClicked.connect(self.get_songs)

    # context menu
    # sets it up so a click allows user to rate/stream/download
    def contextMenuEvent(self, event):
        self.menu = QMenu(self)
        self.rate_act = QAction('Rate', self)
        self.rate_act.triggered.connect(self.rate)
        self.stream_act = QAction('Stream', self)
        self.stream_act.triggered.connect(self.stream)
        self.download_act = QAction('Download', self)
        self.download_act.triggered.connect(self.download)

        self.menu.addAction(self.rate_act)
        self.menu.addAction(self.stream_act)
        self.menu.addAction(self.download_act)
        self.menu.popup(QCursor.pos())

    # takes the chosen album and sends it to the server
    def get_songs(self):
        self.line_edit.setText("Right click a song")
        text = str(self.list.currentItem().text())
        print ("Now in get_songs")
        self.album_name = text
        self.client.send_album(self.album_name, self.artist_id)

    # lists the songs for an album in self.list
    def list_songs(self, line):
        print ("list_songs called")
        songs = line.split("+")
        count = 1
        self.list.clear()
        for x in songs[:-1]:
            self.list.addItem(x)
            count += 1

        self.songs = songs[:-1]
        self.list.doubleClicked.disconnect()
        self.list.itemClicked.connect(self.contextMenuEvent)
