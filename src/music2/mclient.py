import socket
import sys
import os
from pygame import mixer
from globvars import host
from globvars import port
from globvars import bytes

def get_all():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send("-all ")
    dat =  s.recv(bytes)
    s.close()
    return dat


# This sends an artist to the server
# receives the list of albums back in a string
def send_artist(artist_name):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
    except:
        print "Could not connect"
        sys.exit()
    to_send = "-a " + artist_name
    try:
        s.send(to_send)
    except:
        print "Could not connect"
        sys.exit()
    data = s.recv(bytes)
    s.close()
    return data

