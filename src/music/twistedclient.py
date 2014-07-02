from globtwisted import *
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, protocol

class mClient(LineReceiver):
    def __init__(self):
        self.state = ""

    def connectionMade(self):
        print "Connected!"
        self.sendLine("gimme more")

    def lineReceived(self, line):
        print line


class mClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return mClient()

factory = mClientFactory()
reactor.connectTCP(host, port, factory)
reactor.run()

