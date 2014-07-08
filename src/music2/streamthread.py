from PyQt4.QtCore import *

class StreamThread(QThread):
    def __init__(self, bl, streamer):
        QThread.__init__(self)
        self.bl = bl
        self.streamer = streamer
        self.connect(self, SIGNAL("Stop"), self.end)


    def end(self):
        self.streamer.close()


    def __del__(self):
        self.wait()

    def run(self):
        count = 0
        for x in self.bl:
            self.streamer.write(x)
            if count > 40:
                self.bl.remove(x)

