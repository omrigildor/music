from globtwisted import *
from twisted.internet.protocol import Factory, Protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import nItunes
import os
import pymysql


class tServer(LineReceiver):

    # init method
    def __init__(self):
        self.conn = pymysql.connect(host = "localhost", user = "root", passwd = "", db = "test2")
        self.cur = self.conn.cursor()
        self.replies = {
            "-artist" : self.get_artists,
            "-album" : self.get_albums,
            "-rating" : self.rate_song,
            "-download" : self.download,
            "-all" : self.get_all,
            "-size" : self.get_size
        }

    # prints when connected to client
    def connectionMade(self):
        print "Connected to Client"

    #receives the line
    def lineReceived(self, line):
        print line, "received"
        f_choice = line.split(" ")[0]
        func = self.replies.get(f_choice)
        dat = line.split(" ")[1:]
        if func is None:
            print "No function sent"
        else:
            func(dat)

    #sends the full list of artists
    def get_all(self, data):
        self.sendLine("-all-_" + nItunes.get_all(self.cur))

    #sends the albums associated with an artist
    def get_artists(self, data):
        print "artist chosen"
        self.sendLine("-artist-_" + nItunes.get_artists(self.cur, data))

    #sends the songs associated with an album
    # album name, artist_id
    def get_albums(self, data):
        print "album chosen"
        dat = " ".join(data).split("/")
        self.sendLine("-album-_" + nItunes.get_album(self.cur, dat[0], dat[1]))
        
    #sends the rating of a song
    # dat[0] is the chosen song
    # dat[1] is the rating
    # dat[-1] is the artist_id
    def rate_song(self, data):
        print "rating chosen"
        dat = " ".join(data).split("/")
        self.sendLine("-rate-_" + nItunes.rate_song(self.cur, self.conn, dat[0], dat[1], dat[-1]))
        
    # download and stream the song
    # takes song_name
    # artist_id
    def download(self, data):
        dat = " ".join(data).split("/")
        filename = nItunes.download(self.cur, dat[0], dat[1])
        self.read_file(filename)

    # returns the size of the song as a string
    def get_size(self, data):
        dat = " ".join(data)
        self.cur.execute("SELECT size from songs where name = '%s'" % dat)
        f_size = self.cur.fetchall()
        if len(f_size) > 0:
            self.sendLine("-size-_" + str(f_size[0][0]))
        else:
            print dat
            self.sendLine("-size-_15000000")
        
    # reads the mp3 file and sends it line by line to the client
    def read_file(self, filename):
        self.sendLine("-download-_start")
        if os.path.isfile(filename):
            with open(filename, 'r') as infile:
                d = infile.readline()
                while d:
                    self.sendLine(d)
                    d = infile.readline()
        self.sendLine("-stop-_")
        print "Done transfering file"

# the server factory
class mServerFactory(Factory):
    def buildProtocol(self, addr):
        return tServer()

# instantiates factory
# listens on port with that factory
# runs the reactor
factory = mServerFactory()
reactor.listenTCP(port, factory)
reactor.run()
