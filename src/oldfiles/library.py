# Library Class
# takes in a path - location of folder
# lib - the song list
# album - the artist and number of songs list
# biggest, smallest, longest, shortest song

class Library(object):

    numSongs = 0

    def __init__(self, path, lib, albums, sizes, durations):
        self.path = path
        self.lib = lib
        self.albums = albums
        self.sizes = sizes
        self.durations = durations

    def add_artist(self, art, song):
        self.albums.append((art, song))

    def add_song(self, song):
        self.lib.append(song)
        self.sizes.append((song, song.size))
        self.durations.append((song, song.duration))
        self.numSongs += 1

    def sort_biggest(self):
        self.sizes.sort(reverse = True)
        print self.sizes[0][0]

    def sort_longest(self):
        self.durations.sort(reverse = True)
        print self.durations[0][0]

    def sort_artist(self):
        self.albums.sort(reverse = True)
        print self.albums[0][1] + "-" + str(self.albums[0][0])

    def get_letter(self, letter):
        alpha = []
        for x in self.lib:
            alpha.append(x.name)

        alpha.sort()
        res = []

        for ele in alpha:
            if ele.startswith(letter):
                res.append(ele)

        print res

