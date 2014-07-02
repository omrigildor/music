from globtwisted import *
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import nItunes
import os
import thread
import pymysql

conn = pymysql.connect(host = "localhost", user = "root", passwd = "", db = "test2")
cur = conn.cursor()

class mServer(LineReceiver):
        def connectionMade(self):
            self.sendLine("Hello new Client")

        def lineReceived(self, line):
            thread.start_new(self.infinite, ())

        def infinite(self):
            while 1:
                self.sendLine("infinite")


class mServerFactory(Factory):

    def buildProtocol(self, addr):
        return mServer()

factory = mServerFactory()
reactor.listenTCP(port, factory)
reactor.run()
