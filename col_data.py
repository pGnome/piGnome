import sqlite3
import serial

from datetime import datetime

db = sqlite3.connect("myDBfile.sqlite3")

def init_db(cur):
	cur.execute('''CREATE TABLE pGnome (RecordId INTEGER PRIMARY KEY, MoistureLevel INTEGER, GnomeZone INTEGER, CollectedTime TEXT)''')

def insert_db(cur, MoistureLevel, GnomeZone):
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

#xbee input
serialport = serial.Serial("/dev/ttyAMA0", 9600, timeout=5.5)

while True:
  response = serialport.read(size=1)
  response.split('#') #zone,reading
  populate_db(cur, response[1], response[0])
  db.commit()




print_db()
db.close()
