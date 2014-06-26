import os
from optparse import OptionParser
import pymysql
import sys
import urllib2 as URL
import xml.etree.ElementTree as ET

conn = pymysql.connect(host = "localhost", user = "root", passwd = "", db = "t")
cur = conn.cursor()

# takes in an artist name
# runs get_album on the artist name

def get_artists(artist):

    print artist
    artist = ' '.join(artist)
    print artist
    cur.execute("SELECT id from artists where name = '%s'" % artist)
    a_id = cur.fetchone()[0]
    cur.execute("SELECT name from albums where artist_id_fk = " + str(a_id))

    albums = cur.fetchall()
    count = 1
    for al in albums:
        print str(count) + "-" + str(al[0])
        count += 1

    inp = 0
    bl = False
    while not bl:
        try:
            inp = int(
                raw_input("Which album would you like to search (enter a number)\n"))
            if inp <= count - 1:
                bl = True
            else:
                print "Invalid Input"
        except ValueError:
            print "Invalid Input"

    get_album(albums[inp - 1], a_id)

def get_album(album, artist_id):

    cur.execute("SELECT id from albums where name = '%s'" % album)
    al_id = cur.fetchone()
    cur.execute("SELECT name from songs where album_id_fk = '%d'" % al_id)

    songs = cur.fetchall()
    count = 1
    for song in songs:
        print str(count) + "-" + str(song[0])
        count += 1

    inp = 0
    bl = False
    while not bl:
        try:
            inp = int(raw_input("What song would you like to rate? (enter a number)\n"))
            if inp <= count - 1:
                bl = True
            else:
                print "Invalid Input"
        except ValueError:
            print "Invalid Input"

    rating = -1
    bl = False
    while not bl:
        try:
            rating = int(raw_input("What rating? (0 to 5)\n"))
            if rating <= 5 and rating >= 0:
                bl = True
            else :
                print "Invalid Rating"
        except ValueError:
            print "Invalid input"


    chosen = songs[inp - 1][0]
    cur.execute("UPDATE songs set rating = %d where name = '%s' and artist_id_fk = %d" % (rating, chosen, artist_id))
    cur.execute("SELECT name, rating from songs where rating >= 0")
    conn.commit()

def enrich(artist):

    name = ' '.join(artist)
    artist = "%20".join(artist)

    response = URL.urlopen("http://musicbrainz.org/ws/2/artist/?query=artist:" + artist)
    root = ET.fromstring(response.read())


    gender = ""
    country = ""
    disambig = ""
    began = ""
    artist_count = 0
    begin_life = ""
    end_life = ""
    tags = []
    brainz_id = root[0][0].attrib['id']

    for x in root.iter():

        if x.tag.endswith("artist") and artist_count == 1:
            break

        if x.tag.endswith("artist"):
            artist_count += 1

        if x.tag.endswith("disambiguation"):
            disambig = x.text

        if x.tag.endswith("gender"):
            gender = x.text

        if x.tag.endswith("country"):
            country = x.text

        if x.tag.endswith("begin-area"):
            began = x[0].text

        if x.tag.endswith("begin"):
            begin_life = x.text

        if x.tag.endswith("end"):
            end_life = x.text

        if x.tag.endswith("tag"):
            for i in x:
                tags.append(i.text)



    tags = ', '.join(tags)

    if end_life == "":
        end_life = '0000-00-00'

    if gender is None or gender == "":
        gender = "Uknown"

    if country is None or country == "":
        country = "Unknown"

    cur.execute("SELECT * from artists where name = '" + name + "'")
    if cur.fetchall() < 1:
        cur.execute("INSERT into artists (name, gender, country, disambig, begin_area, tags, begin_life, end_life)"
                    "VALUES ('%s','%s','%s','%s','%s','%s','%s')" % name, gender, country, disambig, began, tags, begin_life, end_life, name)
    else:
        cur.execute("UPDATE artists set gender = '%s', country = '%s'"
                ", disambig = '%s', begin_area = '%s', tags = '%s', begin_life = '%s', end_life = '%s' where name = '%s'"
                % (gender, country, disambig, began, tags, begin_life, end_life, name))




    conn.commit()
    enrich_albums(name, brainz_id)


def enrich_albums(artist, brainz_id):

    cur.execute("SELECT id from artists where name = '" + artist + "'")
    a_id = cur.fetchone()[0]

    cur.execute("SELECT name from albums where artist_id_fk = " +str(a_id))
    album_list = cur.fetchall()

    response = URL.urlopen("http://musicbrainz.org/ws/1/artist/" + brainz_id + "?type=xml&inc=sa-Official+release-events")
    root = ET.fromstring(response.read())

    info = dict()


    for x in root.iter():
        if x.attrib.get('type') == "Album Official":
            for i in x:
                if i.tag.endswith("title"):
                    name = i.text

                if i.tag.endswith("release-event-list") and len(i) > 0 and i[0].tag.endswith("event"):
                    info[name] = [i[0].get('date'), i[0].get('format'), i[0].get('country'), x.attrib['id']]



    for i in album_list:
        if info.get(i[0]) is not None:
            cur.execute("UPDATE albums set year = '%s', country = '%s', format = '%s' where name = '%s'"
                        % (info.get(i[0])[0], info.get(i[0])[1], info.get(i[0])[2], i[0]))

    conn.commit()

def enrich_songs(album_id):

    response = URL.urlopen("http://musicbrainz.org/ws/1/release/06355f9d-12a7-4d08-aa10-5ad271b83625?type=xml&inc=tracks")
    root = ET.fromstring(response.read())

    info = []
    for x in root.iter():

        if x.tag.endswith("track-list"):
            for i in x.iter():
                name = ""
                time = 0

                if i.tag.endswith("title"):
                    name = i.text

                if i.tag.endswith("duration"):
                    time = i.text

                info.append((name, time))



def interpret(argv):

    parser = OptionParser()

    parser.add_option("-r", "--rate", action = "store", dest = "artist", help = "choose an artist")

    parser.add_option("-e", "--enrich", action = "store", dest = "enrich", help = "display all artists")

    options = parser.parse_args()

    if sys.argv[1] == "-e" or sys.argv[1] == "--enrich":
        enrich(options[0].enrich.split(" "))

    elif sys.argv[1] == "-r" or sys.argv[1] == "--rate":
        get_artists(options[0].artist.split(" "))


interpret(sys.argv)
