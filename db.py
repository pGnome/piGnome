#Methods associatted with databases#
from parse_rest.connection import register
from parse_rest.datatypes import Object
from datetime import datetime
import serial
import math
import sqlite3

#connect to the parse database#
register("28PBuP52sksBKQskvbMEyny2jVhaECzQ72gyIqsI",
         "ZVYfNMONIiMD9XLEhhUKJqZh4tuHNBRiFPCLnx25")
#mositure history table
class Moisture(Object):
    pass
#moisture setting table
class MoistureSetting(Object):
    pass
#water level table
class Barrel(Object):
    pass

#initialize database#
def init_data_db(cur):
	cur.execute('''CREATE TABLE IF NOT EXISTS pGnome (RecordId INTEGER PRIMARY KEY, MoistureLevel INTEGER, GnomeZone INTEGER, CollectedTime TEXT)''')
def init_setting_db(cur):
	cur.execute('''CREATE TABLE IF NOT EXISTS levelSet (LevelId INTEGER PRIMARY KEY, MoistureLevel INTEGER, SettingTime TEXT, GnomeZone INTEGER)''')
def init_water_db(cur):
	cur.execute('''CREATE TABLE IF NOT EXISTS waterLevel (RecordId INTEGER PRIMARY KEY, waterLevel INTEGER, CollectedTime TEXT)''')
def init_tables():
	unlock_db("myDBfile.sqlite3")
	#connect to the local database#
	myDatabase = sqlite3.connect("myDBfile.sqlite3", check_same_thread=False)
	cur = myDatabase.cursor()
	while True:
		try:
			init_data_db(cur)
			init_setting_db(cur)
			init_water_db(cur)
			break
		except Exception:
			unlock_db("myDBfile.sqlite3")
	try:
		myDatabase.commit()
		myDatabase.close()
	except Exception:
		myDatabase.rollback()

###### MOISTURE LEVEL ######
#check if zone data exist in the table
def row_data_count (cur, GnomeZone):
	cur.execute('''SELECT count(*)
		FROM pGnome
		WHERE GnomeZone = ?
		''',(GnomeZone,))
	return cur.fetchall()[0]
#inserting data from moisture sensors#
def insert_db(cur, MoistureLevel, GnomeZone):
	cur.execute('''INSERT INTO pGnome
		(RecordId, MoistureLevel, GnomeZone, CollectedTime)
		VALUES (NULL,?,?,?)''', (MoistureLevel, GnomeZone, datetime.now()))
#update data from moisture sensors#
def update_db(cur, MoistureLevel, GnomeZone):
	cur.execute('''UPDATE levelSet
		SET MoistureLevel = ?, CollectedTime = ?
		WHERE GnomeZone = ?''', (MoistureLevel, datetime.now(), GnomeZone))
	print cur.fetchall()
#main method to collect current mositure level data#
def data_collect(identifier, txt=''):
	unlock_db("myDBfile.sqlite3")
	#connect to the local database#
	myDatabase = sqlite3.connect("myDBfile.sqlite3", check_same_thread=False)
	cur = myDatabase.cursor()
	#xbee input
	serialport = serial.Serial("/dev/ttyAMA0", 9600, timeout=5.5)
	response = serialport.read(size=24)
  	if response.__len__() == 24:
		#parse channel number and moisture data from the packet
		channelRaw = ord(response[4])
		if channelRaw > 0:
			channel = channelRaw / 17
			print channel
			data = ord(response[11]) * 256 + ord(response[12]) + 1
			level = int(data*100/1024)
			print level
			while True:
				try:
					if row_data_count(cur,channel)[0] == 0:
						insert_db(cur, level, channel)
					else:
						update_db(cur, level, channel)
					break
				except Exception:
					unlock_db("myDBfile.sqlite3")
			
	try:
		myDatabase.commit()
		myDatabase.close()
	except Exception:
		myDatabase.rollback()

	#print identifier

###### WATER LEVEL ######
#check if water level data exist in the table
def row_water_count (cur):
	cur.execute('''SELECT count(*)
		FROM waterLevel
		''')
	return cur.fetchall()[0]
#inserting data from moisture sensors#
def insert_water_db(cur, waterLevel):
	cur.execute('''INSERT INTO waterLevel
		(RecordId, waterLevel, CollectedTime)
		VALUES (NULL,?,?)''', (waterLevel, datetime.now()))
#update data from moisture sensors#
def update_water_db(cur, waterLevel):
	cur.execute('''UPDATE waterLevel
		SET MoistureLevel = ?, CollectedTime = ?
		WHERE RecordId = 1''', (waterLevel, datetime.now()))

#main method to collect current water level data#
def data_water_collect(identifier, txt=''):
	unlock_db("myDBfile.sqlite3")
	#connect to the local database#
	myDatabase = sqlite3.connect("myDBfile.sqlite3", check_same_thread=False)
	cur = myDatabase.cursor()

	while True:
		try:
			if row_water_count(cur)[0] == 0:
				insert_water_db(cur, level)
			else:
				update_water_db(cur, level)
			break
		except Exception:
			unlock_db("myDBfile.sqlite3")
			
	try:
		myDatabase.commit()
		myDatabase.close()
	except Exception:
		myDatabase.rollback()

	# print identifier


###### MOISTURE SETTING ######
#updating the current moisture level setting#
def row_count (cur, GnomeZone):
	cur.execute('''SELECT count(*)
		FROM levelSet
		WHERE GnomeZone = ?
		''',(GnomeZone,))
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
#main function to update the current moisture level setting#
def moisture_setting(identifier, txt=''):
	unlock_db("myDBfile.sqlite3")
	#connect to the local database#
	myDatabase = sqlite3.connect("myDBfile.sqlite3", check_same_thread=False)
	cur = myDatabase.cursor()
	for GnomeZone in range (1,4):
		recentSet = MoistureSetting.Query.filter(gnomeZone=GnomeZone).order_by("-createdAt")
		recentOne = recentSet.limit(1)
		for ob in recentOne:
			while True:
				try:
					if row_count(cur,GnomeZone)[0] == 0:
						insert_setting_db(cur,ob.level,ob.createdAt,ob.gnomeZone)
					else:
						update_setting_db(cur,ob.level,ob.createdAt,ob.gnomeZone)
					cur.execute('''SELECT *
						FROM levelSet
						''')
					for record in cur.fetchall():
						print record
					break
				except Exception:
					unlock_db("myDBfile.sqlite3")
	try:
		myDatabase.commit()
		myDatabase.close()
	except Exception:
		myDatabase.rollback()

	# print identifier


###### SYNCING DATABASE ######
#pushing data from local database to parse database#
def update_remote_db(identifier,txt=''):
	unlock_db("myDBfile.sqlite3")
	#connect to the local database#
	myDatabase = sqlite3.connect("myDBfile.sqlite3", check_same_thread=False)
	cur = myDatabase.cursor()
	while True:
		try:
			cur.execute('''SELECT *
				FROM pGnome
				''')
			for record in cur.fetchall():
				gnomeScore = Moisture(level=record[1], gnomeZone=int(record[2]), collectedTime=record[3])
				gnomeScore.save()
				print record
			break
		except Exception:
			unlock_db("myDBfile.sqlite3")

	try:
		myDatabase.commit()
		myDatabase.close()
	except Exception:
		myDatabase.rollback()
	
	# print identifier

#prevent database locking issue
def unlock_db(db_filename):
    connection = sqlite3.connect(db_filename)
    connection.commit()
    connection.close()
