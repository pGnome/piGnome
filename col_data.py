import sqlite3
import serial

from datetime import datetime

db = sqlite3.connect("myDBfile.sqlite3")

#create moisture level data table
def init_db(cur):
	cur.execute('''CREATE TABLE IF NOT EXISTS pGnome (RecordId INTEGER PRIMARY KEY, MoistureLevel INTEGER, GnomeZone INTEGER, CollectedTime TEXT)''')

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
  response = serialport.read(size=26)
  if response.__len__() > 0:
	#parse channel number and moisture data from the packet
	channel = ord(response[11])
	data = ord(response[13]) * 256 + ord(response[14])
  	populate_db(cur, data, channel)
  	db.commit()


print_db()
db.close()
