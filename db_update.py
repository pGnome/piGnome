from parse_rest.connection import register
from parse_rest.datatypes import Object
from parse_rest.user import User
import serial
import sqlite3
import math
import time
from datetime import datetime

register("28PBuP52sksBKQskvbMEyny2jVhaECzQ72gyIqsI",
		 "ZVYfNMONIiMD9XLEhhUKJqZh4tuHNBRiFPCLnx25")

currentUser = User.login("testPi", "raspberry")
#print(currentUser.objectId)

#parse tables
#moisture setting table
class MoistureSetting(Object):
    pass

db = sqlite3.connect("myDBfile.sqlite3")

#initialize database#
def init_data_db(cur):
	cur.execute('''CREATE TABLE IF NOT EXISTS pGnome (RecordId INTEGER PRIMARY KEY, MoistureLevel INTEGER, GnomeZone INTEGER, CollectedTime TEXT)''')
def init_setting_db(cur):
	cur.execute('''CREATE TABLE IF NOT EXISTS levelSet (LevelId INTEGER PRIMARY KEY, MoistureLevel INTEGER, SettingTime TEXT, GnomeZone INTEGER)''')
def init_tables(cur):
	init_data_db(cur)
	init_setting_db(cur)


#collecting data from moisture sensors#

def insert_db(cur, MoistureLevel, GnomeZone):
	cur.execute('''INSERT INTO pGnome
		(RecordId, MoistureLevel, GnomeZone, CollectedTime)
		VALUES (NULL,?,?,?)''', (MoistureLevel, GnomeZone, datetime.now()))

def data_collect(cur):
	#xbee input
	serialport = serial.Serial("/dev/ttyAMA0", 9600, timeout=5.5)
	response = serialport.read(size=26)
  	if response.__len__() > 0:
		#parse channel number and moisture data from the packet
		channel = math.log(ord(response[11]),2)
		data = ord(response[13]) * 256 + ord(response[14]) + 1
		level = int(data*100/1024)
		insert_db(cur, level, channel)


#retrieve setting from parse database#

#updating the current moisture level setting
def row_count (cur, GnomeZone):
	cur.execute('''SELECT count(*)
		FROM levelSet
		WHERE GnomeZone = ?
		''',())
	return cur.fetchall()[0]
#insert
def insert_setting_db(cur, MoistureLevel, SettingTime, GnomeZone):
	cur.execute('''INSERT INTO levelSet
		(LevelId, MoistureLevel, SettingTime, GnomeZone)
		VALUES (NULL,?,?,?)''', (MoistureLevel, SettingTime, GnomeZone))
#update
def update_setting_db(cur, MoistureLevel, SettingTime, GnomeZone):
	cur.execute('''UPDATE levelSet
		SET MoistureLevel = ?, SettingTime = ?
		WHERE GnomeZone = ?''', (MoistureLevel, SettingTime, GnomeZone))
def moisture_setting(cur):
	for GnomeZone in range (1,3):
		recentSet = MoistureSetting.Query.filter(gnomeZone=GnomeZone).order_by("-createdAt")
		recentOne = recentSet.limit(1)
		for ob in recentOne:
			#print ob.user
			if row_count(cur,GnomeZone)[0] == 0:
				insert_setting_db(cur,ob.level,ob.createdAt,ob.gnomeZone)
			else:
				update_setting_db(cur,ob.level,ob.createdAt,ob.gnomeZone)

#print out current data table#
def print_db(cur):
	cur.execute('''SELECT *
		FROM pGnome
		''')
	print cur.fetchall()

cur = db.cursor()
init_tables(cur)

count = 0
while count < 250:
	data_collect(cur)
	db.commit()
	moisture_setting(cur)
	db.commit()
	print_db(cur)
	count += 1


db.commit()
db.close()
