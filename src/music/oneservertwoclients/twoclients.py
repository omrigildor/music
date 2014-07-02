from twisted.internet import reactor, protocol

HOST = 'localhost'
PORT = 9001

class MyClient(protocol.Protocol):
    def connectionMade(self):
        self.transport.write("Send me a poem")

    def dataReceived(self, data):
        print "data received"
        print data
        self.transport.loseConnection()

class MyClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return MyClient()

factory = MyClientFactory()
reactor.connectTCP(HOST, PORT, factory)
reactor.run()