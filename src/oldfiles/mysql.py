__author__ = 'omrigildor'
import pymysql


conn = pymysql.connect(host = "localhost", user = "root", passwd = "", db = "test2")

cur = conn.cursor()
with conn:
    (cur.execute("SELECT id FROM artists where name = 'Kanye West'"))
    print (cur.fetchone())[0]
    cur.execute("SELECT name from albums where artist_id_fk = 13")
    print (cur.fetchone())