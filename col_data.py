import sqlite3
from datetime import datetime

db = sqlite3.connect("myDBfile.sqlite3")

def init_db(cur):
	cur.execute('''CREATE TABLE pGnome (RecordId INTEGER PRIMARY KEY, MoistureLevel INTEGER, GnomeZone INTEGER, CollectedTime TEXT)''')

def populate_db(cur, MoistureLevel, GnomeZone):
	cur.execute('''INSERT INTO pGnome
		(RecordId, MoistureLevel, GnomeZone, CollectedTime)
		VALUES (NULL,?,?,?)''', (MoistureLevel, GnomeZone, datetime.now()))
	print '1'

def print_db():
	cur.execute('''SELECT * 
		FROM pGnome
		''')
	print cur.fetchall()

cur = db.cursor()
init_db(cur)
populate_db(cur, 50, 1)
populate_db(cur, 30, 2)
db.commit()
print_db()
db.close()
