from PyQt4.QtCore import *
import time

class StreamThread(QThread):
    go = True
    position = 0

    def __init__(self, bl, streamer, p):
        QThread.__init__(self)
        self.bytelist = bl
        self.streamer = streamer
        self.p = p
        self.connect(self, SIGNAL("Stop"), self.end)


    def end(self):
        print "Ending"
        self.go = False
        self.emit(SIGNAL("Pause"))
        self.streamer.close()
        self.p.terminate()


    def __del__(self):
        self.wait()

    def run(self):
        for x in self.bytelist:
            if self.go:
                try:
                    self.position += len(x)
                    self.streamer.write(x)
                except:
                    print "Some overflow error"


