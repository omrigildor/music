import socket
import nItunes
import os
from globvars import host
from globvars import port
from nItunes import cur
from globvars import bytes




s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((host, port))

s.listen(10)

replies = {
    "-a" : nItunes.get_artists,
    "-c" : nItunes.get_album,
    "-r" : nItunes.get_song,
    "-d" : nItunes.download,
    "-all" : nItunes.get_all

}

while True:

    print "Running"
    connect, addr = s.accept()
    data = connect.recv(bytes)
    func = replies.get(data.split(" ")[0])
    to_ret = ""
    print data
    print "Before Choices"
    print "Choice ", data.split(" ")[0]

    if data.split(" ")[0] == "-a":
        print data.split(" ")[1:]
        print "single artist"
        to_ret = func(data.split(" ")[1:])

    elif data.split(" ")[0] == "-all":
        print "all artists"
        to_ret = func()

    elif data.split(" ")[0] == "-c":
        print "all albums"
        data = data.split(" ")[1:]
        data = " ".join(data)
        data = data.split("/")
        to_ret = func(data[0], data[1])

    elif data.split(" ")[0] == "-r":
        print "rating"
        data = data.split(" ")[1:]
        data = " ".join(data)
        data = data.split("/")
        to_ret = func(data[0], data[1], data[-1])


    elif data.split(" ")[0] == "-d":
        print "dl/stream"
        data = data.split(" ")[1:]
        data = " ".join(data)
        data = data.split("/")
        filename = func(data[0], data[1])
        if os.path.exists(filename):
            with open(filename, 'r') as infile:
                d = infile.read(bytes)
                while d:
                    connect.send(d)
                    d = infile.read(bytes)

    if not data:
        break

    connect.sendall(to_ret)

    connect.close()

s.close()
