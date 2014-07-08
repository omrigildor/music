__author__ = 'omrigildor'
import mainwindow
import qt4reactor
from PyQt4.QtGui import *
import sys
import qt4reactor

app = QApplication(sys.argv)
qt4reactor.install()
from twisted.internet import reactor
nS = mainwindow.nSpotify(reactor)
nS.show()
reactor.run()