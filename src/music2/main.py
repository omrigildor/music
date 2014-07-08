__author__ = 'omrigildor'
import nspotify
import qt4reactor
from PyQt4.QtGui import *
import sys
import qt4reactor

app = QApplication(sys.argv)
qt4reactor.install()
from twisted.internet import reactor
nS = nspotify.nSpotify(reactor)
nS.show()
reactor.run()