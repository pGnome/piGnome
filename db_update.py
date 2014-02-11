from parse_rest.connection import register
from parse_rest.datatypes import Object
import sqlite3
import time
from threading import Timer
from datetime import datetime

register("28PBuP52sksBKQskvbMEyny2jVhaECzQ72gyIqsI",
		 "ZVYfNMONIiMD9XLEhhUKJqZh4tuHNBRiFPCLnx25")

#parse tables
#mositure history table
class Moisture(Object):
    pass
#moisture setting table
class MoistureSetting(Object):
    pass

db = sqlite3.connect("myDBfile.sqlite3")

#initialize database#
def init_data_db(cur):
	cur.execute('''CREATE TABLE IF NOT EXISTS pGnome (RecordId INTEGER PRIMARY KEY, MoistureLevel INTEGER, GnomeZone INTEGER, CollectedTime TEXT)''')
def init_setting_db(cur):
	cur.execute('''CREATE TABLE IF NOT EXISTS levelSet (LevelId INTEGER PRIMARY KEY, MoistureLevel INTEGER, SettingTime TEXT)''')
def init_tables(cur):
	init_data_db(cur)
	init_setting_db(cur)


#collecting data from moisture sensors#

def insert_db(cur, MoistureLevel, GnomeZone):
	cur.execute('''INSERT INTO pGnome
		(RecordId, MoistureLevel, GnomeZone, CollectedTime)
		VALUES (NULL,?,?,?)''', (MoistureLevel, GnomeZone, datetime.now()))
	print '1'

def data_collect(cur):
	init_data_db(cur)
	#xbee input
	serialport = serial.Serial("/dev/ttyAMA0", 9600, timeout=5.5)
	response = serialport.read(size=1)
  	response.split('#') #zone,reading
  	insert_db(cur, response[1], response[0])

#pushing data from local database to parse database#
def update_remote_db(cur):
	cur.execute('''SELECT *
		FROM pGnome
		''')
	for record in cur.fetchall():
		gnomeScore = pGnomeTest(level=record[1], gnomeZone=record[2], collectedTime=record[3])
		gnomeScore.save()

#retrieve setting from parse database#

#updating the current moisture level setting
def collect_db(cur, MoistureLevel, SettingTime):
	cur.execute('''INSERT INTO levelSet
		(LevelId, MoistureLevel, SettingTime)
		VALUES (NULL,?,?)''', (MoistureLevel, SettingTime))
def moisture_setting(cur):
	init_setting_db(cur)
	recentSet = MoistureSetting.Query.all().order_by("-createdAt")
	recentOne = recentSet.limit(1)

	for ob in recentOne:
		collect_db(cur,ob.level,ob.createdAt)


def print_db():
	cur.execute('''SELECT *
		FROM pGnome
		''')
	print cur.fetchall()

cur = db.cursor()
init_tables(cur)

while True:
	Timer(1, data_collect, (cur)).start()
	Timer(1, moisture_setting, (cur)).start()
	Timer(60, update_remote_db, (cur)).start()

db.commit()

print_db()
db.close()
