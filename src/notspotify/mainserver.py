from twistedserver import mServerFactory
from twisted.internet import reactor
from constants import *
# instantiates factory
# listens on port with that factory
# runs the reactor
factory = mServerFactory()
reactor.listenTCP(port, factory)
reactor.run()
