from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver

import os
PORT = 9001

poem = open("/Users/omrigildor/twisted-intro/poetry/science.txt", "rb")

class MyServer(LineReceiver):
    def connectionMade(self):
        print "Connected to a client"

    def lineReceived(self, line):
        print "received ", data
        x = poem.readline()
        print "Sending"
        while x != "":
            self.sendLine(x)
            x = poem.readline()
        print "done"

class MyServerFactory(protocol.Factory):
    protocol = MyServer

factory = MyServerFactory()
reactor.listenTCP(PORT, factory)
reactor.run()