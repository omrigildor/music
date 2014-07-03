
import urllib2 as URL
import xml.etree.ElementTree as ET



# takes in an artist name
# runs get_album on the artist name
def enrich_all(cur, conn):
    cur.execute("SELECT name from artists")
    names = cur.fetchall()
    cur.execute("SELECT name from albums")
    albums = cur.fetchall()

    for a in names:
        enrich(cur, conn, a[0].split(" "))


#returns all the data associated with all artists in the db
def get_all(cur):
    cur.execute("SELECT name, gender, country, begin_area, tags from artists")
    names = cur.fetchall()

    artists = ""
    for a in names:
        for i in a:
            artists += str(i) + "/"
        artists += "+"


    return artists

#returns the list of albums for an artist
def get_artists(cur, artist):

    artist = ' '.join(artist)
    print artist
    cur.execute("""SELECT id from artists where name = "%s" """ % artist)
    a_id = cur.fetchone()[0]
    cur.execute("SELECT name from albums where artist_id_fk = " + str(a_id))

    albums = cur.fetchall()
    album_str = ""
    for al in albums:
        album_str += al[0] + "+"


    return album_str + str(a_id)

#gets all the songs from an album
def get_album(cur, album, artist):

    artist_id = int(artist)
    cur.execute("""SELECT id from albums where name = "%s" and artist_id_fk = %d""" % (album, artist_id))
    al_id = cur.fetchone()[0]

    cur.execute("""SELECT name from songs where album_id_fk = %d""" % al_id)
    songs = cur.fetchall()
    song_str = ""

    for song in songs:
        song_str += song[0] + "+"

    return song_str

#updates a rating of a song
def rate_song(cur, conn, chosen , rating, artist_id):

    cur.execute("""UPDATE songs set rating = %f where name = "%s" and artist_id_fk = %d""" % (float(rating), chosen, int(artist_id)))
    conn.commit()
    return "Updated Rating of %s to %s" % (chosen, rating)


def enrich(cur, conn, artist):

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

    if len(end_life) <= 4:
        end_life += "-00-00"

    if gender is None or gender == "":
        gender = "Uknown"

    if country is None or country == "":
        country = "Unknown"

    if begin_life == "":
        begin_life = '0000-00-00'

    if len(begin_life) == 4:
        begin_life += ("-00-00")

    cur.execute("""SELECT * from artists where name = %s """ % name)
    if cur.fetchall() < 1:
        cur.execute("""INSERT into artists (name, gender, country, disambig, begin_area, tags, begin_life, end_life)"
                    "VALUES ("%s","%s","%s","%s","%s","%s","%s")""" % name, gender, country, disambig, began, tags, begin_life, end_life, name)
    else:
        cur.execute("""UPDATE artists set gender = "%s", country = "%s", disambig = "%s", begin_area = "%s", tags = "%s", begin_life = "%s", end_life = "%s" where name = "%s" """
                % (gender, country, disambig, began, tags, begin_life, end_life, name))




    conn.commit()
    enrich_albums(name, brainz_id)


def enrich_albums(cur, conn, artist, brainz_id):

    cur.execute("""SELECT id from artists where name = %s""" % artist)
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
            cur.execute("""UPDATE albums set year = "%s", format = "%s", country = "%s" where name = "%s" """
                        % (info.get(i[0])[0], info.get(i[0])[1], info.get(i[0])[2], i[0]))

    conn.commit()

def download(cur, song, artist_id):
    cur.execute("""SELECT path from songs where name = "%s" and artist_id_fk = %d""" % (song, int(artist_id)))
    path = cur.fetchone()[0]
    return path

