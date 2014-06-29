import os
import pymysql
from mutagen.mp3 import MP3
import re
import sys
import urllib2 as URL
import xml.etree.ElementTree as ET

def get_library(loc):

    os.chdir(os.path.abspath(loc))
    path = os.path.abspath(loc)
    conn = pymysql.connect(host = "localhost", user = "root", passwd = "", db = "test2")
    cur = conn.cursor()
    art = ""
    last_id = 0
    for mp in os.listdir(path)[1:]:

        artist = mp.split(" - ")[0]

        if artist != art:
            with conn:
                cur.execute("INSERT into artists (name) VALUES('%s')" % artist)
            a_id = conn.insert_id()
        else:
            a_id = last_id

        if os.path.isdir(mp):
            album = mp.split(" - ")[1]
            with conn:
                cur.execute("INSERT into albums (name, artist_id_fk) VALUES('%s', %d)" % (album, a_id))
            al_id = conn.insert_id()
            for i in os.listdir(mp):

                if i.split(".")[-1] == "mp3":
                    pwd = path + "/" + mp + "/" + i
                    size = os.path.getsize(pwd)
                    duration = MP3(pwd).info.length
                    name = i
                    pwd = pwd
                    with conn:
                        cur.execute("INSERT into songs (name, size, length, path, artist_id_fk, album_id_fk)"
                                    "VALUES('%s', %d, %d, '%s', %d, %d)" % (name, size, duration, pwd, a_id, al_id))


        elif mp.split(".")[-1] == "mp3":

            name = mp

            pwd = path + "/" + mp
            size = os.path.getsize(path + "/" + mp)
            duration = MP3(path + "/" + mp).info.length

            with conn:
                cur.execute("INSERT into songs (name, size, length, path, artist_id_fk)"
                            "VALUES('%s', %.2d, %d, '%s', %d)" % (name, size, duration, pwd, a_id))
        art = artist
        last_id = a_id

get_library("/Users/omrigildor/Downloads/Music")