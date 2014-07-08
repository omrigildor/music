from twisted.internet import protocol
from struct import pack, unpack


class tClient(protocol.Protocol):

    down = False
    stream = False
    info = False
    dumb = True
    open = True
    count = 0
    wt = 0
    data = ""
    opening = ""

    def __init__(self, gui):
        self.gui = gui

    def set_thread(self, wthread):
        self.wt = wthread

    def connectionMade(self):
        print "Connected!"
        self.get_all()
        self.gui.set_client(self)

    # receives data from the server
    def dataReceived(self, data):
        if "-stop-_" in data and self.down:
            self.gui.download_finish()
            self.down = False

        elif self.stream:
            self.data += data
            if len(self.data) > 441000:
                if self.dumb:
                    self.count = 0
                    if self.open:
                        self.wt.bl.append(self.data)
                        self.opening = self.data[:44]
                        self.open = False
                    else:
                        self.wt.bl.append(self.data)


                    print "Not Dumb"
                    self.dumb = False
                    self.gui.play_stream()

                else:
                    self.wt.bl.append(self.data)

                self.data = ""

        elif self.down:
            self.gui.download_test(data)

        else:
            for x in data.split("\r\n"):
                if x != "" and "-_" in x:
                    self.processData(x)


    def processData(self, data):
        x = data.split("-_")
        choice = x[0]
        lin = x[1]
        if choice == "-all":
            # this runs the gui get_artists with all the artists
            self.gui.list_artists(lin)

        elif choice == "-information":
            dat = lin.split("_")
            print dat
            self.gui.set_info(dat[0], dat[1], dat[2], dat[3])

        elif choice == "-artist":
            # data is now the list of albums
            self.gui.list_albums(lin)

        elif choice == "-album":
            # data is the list of songs
            self.gui.list_songs(lin)

        elif choice == "-rate":
            # data is the updated rating
            self.gui.update_text(lin)

        elif choice == "-download":
            self.down = True

        elif choice == "-stream":
            self.data = ""
            self.dumb = True
            self.stream = True

        elif choice == "-size":
            self.gui.set_filesize(int(lin))

        elif choice == "-streamstop":
            self.wt.bl.append(data)
            self.stream = False






    #tells the server to send the full list of artists
    def get_all(self):
        self.transport.write("-all ")
        self.transport.write("\r\n")

    # tells the server to send the albums for a given artist
    def send_artist(self, artist_name):
        self.transport.write("-artist " + artist_name)
        self.transport.write("\r\n")

    # tells the server to send the songs for an album
    def send_album(self, album_name, artist_id):
        self.transport.write("-album " + album_name + "/" + artist_id)
        self.transport.write("\r\n")

    # gives a rating to the server
    def send_rating(self, song_name, rating, artist_id):
        self.transport.write("-rating " + song_name + "/" + rating + "/" + artist_id)
        self.transport.write("\r\n")

    # gets the size of a song
    def get_song_size(self, song_name):
        self.transport.write("-size %s" % song_name)
        self.transport.write("\r\n")
    def download_song(self, song_name, artist_id):
        self.transport.write("-download %s/%s" % (song_name, artist_id))
        self.transport.write("\r\n")

    def stream_song(self, song_name, artist_id, index = 0):
        self.transport.write("-stream %s/%s/%d" % (song_name, artist_id, index))
        self.transport.write("\r\n")
        self.data = ""

    def get_info(self, song_name, artist_id):
        self.transport.write("-info %s/%s" % (song_name, artist_id))
        self.transport.write("\r\n")

# client factory
class mClientFactory(protocol.ClientFactory):
    def __init__(self, gui):
        self.gui = gui

    def buildProtocol(self, addr):
        return tClient(self.gui)



