__author__ = 'omrigildor'
import moregui
import twistedclient

import qt4reactor
from PyQt4.QtGui import *
import sys
import qt4reactor

app = QApplication(sys.argv)
qt4reactor.install()
from twisted.internet import reactor
nS = moregui.nSpotify(reactor)
nS.show()
reactor.run()