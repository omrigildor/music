# Song class
# name, artist, album, duration, and size of the song
class Song(object):

    def __init__(self, name="", artist="",
                 album="", duration=0, size=0):
        self.artist = artist
        self.duration = duration
        self.size = size
        self.name = name

    def __str__(self):
        return str(self.size) + " " + str(self.duration) \
               + " " +  self.name + "-" + self.artist

