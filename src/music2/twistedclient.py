from twisted.protocols.basic import LineReceiver
from twisted.internet import protocol


class tClient(LineReceiver):

    down = False
    def __init__(self, gui):
        self.gui = gui

    def connectionMade(self):
        print "Connected!"
        self.get_all()
        self.gui.set_client(self)

    # receives data from the server
    def lineReceived(self, line):
        if line == "-stop-_":
            self.down = False
            self.gui.download_finish()

        elif self.down:
            self.gui.download_test(line)
        else:
            choice = line.split("-_")[0]
            lin = line.split("-_")[1]
            if choice == "-all":
                # this runs the gui get_artists with all the artists
                self.gui.list_artists(lin)

            elif self.down:
                self.gui.download_test()

            elif choice == "-artist":
                # line is now the list of albums
                self.gui.list_albums(lin)

            elif choice == "-album":
                # line is the list of songs
                self.gui.list_songs(lin)

            elif choice == "-rate":
                # line is the updated rating
                self.gui.update_text(lin)

            elif choice == "-download":
                self.down = True

            elif choice == "-size":
                self.gui.set_filesize(int(lin))


    #tells the server to send the full list of artists
    def get_all(self):
        self.sendLine("-all ")

    # tells the server to send the albums for a given artist
    def send_artist(self, artist_name):
        self.sendLine("-artist " + artist_name)

    # tells the server to send the songs for an album
    def send_album(self, album_name, artist_id):
        self.sendLine("-album " + album_name + "/" + artist_id)

    # gives a rating to the server
    def send_rating(self, song_name, rating, artist_id):
        self.sendLine("-rating " + song_name + "/" + rating + "/" + artist_id)

    # gets the size of a song
    def get_song_size(self, song_name):
        self.sendLine("-size %s" % song_name)

    def download_song(self, song_name, artist_id):
        self.sendLine("-download %s/%s" % (song_name, artist_id))

# client factory
class mClientFactory(protocol.ClientFactory):
    def __init__(self, gui):
        self.gui = gui

    def buildProtocol(self, addr):
        return tClient(self.gui)



