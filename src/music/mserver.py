import socket
import nItunes
import os
from globvars import host
from globvars import port
from globvars import bytes
import thread
import pymysql


conn = pymysql.connect(host = "localhost", user = "root", passwd = "", db = "test2")
cur = conn.cursor()

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

def readFile(filename, fktuples):
    if os.path.isfile(filename):
        with open(filename, 'r') as infile:
            d = infile.read(bytes)
            while d:
                connect.send(d)
                d = infile.read(bytes)
    connect.sendall(to_ret)
    connect.close()

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
        to_ret = func(cur, data.split(" ")[1:])
        connect.sendall(to_ret)
        connect.close()


    elif data.split(" ")[0] == "-all":
        print "all artists"
        to_ret = func(cur)
        connect.sendall(to_ret)
        connect.close()

    elif data.split(" ")[0] == "-c":
        print "all albums"
        data = data.split(" ")[1:]
        data = " ".join(data)
        data = data.split("/")
        to_ret = func(cur, data[0], data[1])
        connect.sendall(to_ret)
        connect.close()

    elif data.split(" ")[0] == "-r":
        print "rating"
        data = data.split(" ")[1:]
        data = " ".join(data)
        data = data.split("/")
        to_ret = func(cur, conn, data[0], data[1], data[-1])
        connect.sendall(to_ret)
        connect.close()


    elif data.split(" ")[0] == "-d":
        print "dl/stream"
        data = data.split(" ")[1:]
        data = " ".join(data)
        data = data.split("/")
        filename = func(cur, data[0], data[1])
        thread.start_new_thread(readFile, (filename, ''))

    elif data.split(" ")[0] == "-gi":
        print " ".join(data.split(" ")[1:])
        cur.execute("SELECT size from songs where name = '%s'" % " ".join(data.split(" ")[1:]))
        f_size = cur.fetchall()
        print f_size
        if len(f_size) > 0:
            to_ret = str(f_size[0][0])
        else:
            to_ret = "15000000"
        connect.sendall(to_ret)
        connect.close()

    if not data:
        break

s.close()
