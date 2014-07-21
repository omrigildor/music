from constants import *
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import threads
import dbutils
import os
import pymysql
from pydub import AudioSegment
import wave
import pyaudio

class tServer(LineReceiver):

    # init method
    files = []
    def __init__(self):
        print "Server is Running"
        self.conn = pymysql.connect(host = "localhost", user = "root", passwd = "", db = "test2")
        self.cur = self.conn.cursor()
        self.replies = {
            "-artist" : self.get_artists,
            "-album" : self.get_albums,
            "-rating" : self.rate_song,
            "-download" : self.download,
            "-all" : self.get_all,
            "-size" : self.get_size,
            "-stream" : self.stream,
            "-info" : self.get_information
        }

    # prints when connected to client
    def connectionMade(self):
        print "Connected to Client"


    #receives the line
    def dataReceived(self, data):
        for x in data.split("\r\n"):
            if x != "":
                self.processData(x)

    def processData(self, data):
        print data, "received"
        f_choice = data.split(" ")[0]
        func = self.replies.get(f_choice)
        dat = data.split(" ")[1:]
        if func is None:
            print "No function sent"
        else:
            func(dat)

    #sends the full list of artists
    def get_all(self, data):
        self.transport.write("-all-_" + dbutils.get_all(self.cur) + "\r\n")

    #sends the albums associated with an artist
    def get_artists(self, data):
        print "artist chosen"
        self.transport.write("-artist-_" + dbutils.get_artists(self.cur, data) + "\r\n")

    #sends the songs associated with an album
    # album name, artist_id
    def get_albums(self, data):
        print "album chosen"
        dat = " ".join(data).split("/")
        self.transport.write("-album-_" + dbutils.get_album(self.cur, dat[0], dat[1]) + "\r\n")


    def get_information(self, data):
        print "Getting data"
        dat = " ".join(data).split("/")
        filename = dbutils.download(self.cur, dat[0], dat[1])
        ex_file = filename.split(".mp3")[0] + ".wav"
        if os.path.isfile(filename):
            sound = AudioSegment.from_mp3(filename)
            sound.export(ex_file, format="wav")
        p = pyaudio.PyAudio()
        size = os.stat(ex_file).st_size
        w = wave.open(ex_file, "r")
        width = p.get_format_from_width(w.getsampwidth())
        frames = w.getnframes()
        rate = w.getframerate()
        chan = w.getnchannels()
        self.transport.write("-information-_%d_%d_%d_%d\r\n" % (width, chan, rate, size))



    #sends the rating of a song
    # dat[0] is the chosen song
    # dat[1] is the rating
    # dat[-1] is the artist_id
    def rate_song(self, data):
        print "rating chosen"
        dat = " ".join(data).split("/")
        self.transport.write("-rate-_" + dbutils.rate_song(self.cur, self.conn, dat[0], dat[1], dat[-1]) + "\r\n")
        
    # download and stream the song
    # takes song_name
    # artist_id
    def download(self, data):
        dat = " ".join(data).split("/")
        filename = dbutils.download(self.cur, dat[0], dat[1])
        threads.deferToThread(self.read_file, filename)

    # stream a song
    def stream(self, data):
        dat = " ".join(data).split("/")
        filename = dbutils.download(self.cur, dat[0], dat[1])
        threads.deferToThread(self.stream_file, filename, dat[-1])

    # returns the size of the song as a string
    def get_size(self, data):
        print "getting size"
        dat = " ".join(data)
        self.cur.execute("SELECT size from songs where name = '%s'" % dat)
        f_size = self.cur.fetchall()
        if len(f_size) > 0:
            self.song_size = f_size[0][0]
            self.transport.write("-size-_" + str(f_size[0][0]) + "\r\n")
        else:
            print dat, "Error"

        
    # reads the mp3 file and sends it line by line to the client
    def read_file(self, filename):
        print "Download Start"
        self.transport.write("-download-_start\r\n")
        ex_file = filename.split(".mp3")[0] + ".wav"
        if os.path.isfile(filename):
            sound = AudioSegment.from_mp3(filename)
            sound.export(ex_file, format="wav")
            with open(ex_file, 'r') as infile:
                d = infile.read(1024)
                while d:
                    self.transport.write(d)
                    d = infile.read(1024)
        self.transport.write("-stop-_\r\n")
        os.remove(ex_file)
        print "Done downloading file"

    #STREAMS THE MP3 FILE
    def stream_file(self, filename, index):
        print "Streaming start"
        self.transport.write("-stream-_start\r\n")
        ex_file = filename.split(".mp3")[0] + ".wav"
        if os.path.isfile(filename):
            sound = AudioSegment.from_mp3(filename)
            sound.export(ex_file, format="wav")
            with open(ex_file, 'r') as infile:
                infile.seek(int(index))
                d = infile.read(1024)
                while d: #1740800 ~ 10 sec
                    self.transport.write(d)
                    d = infile.read(1024)

        self.files.append(ex_file)

        self.transport.write("\r\n-streamstop-_\r\n")
        print "Done streaming file"


# the server factory
class mServerFactory(Factory):
    def buildProtocol(self, addr):
        return tServer()


