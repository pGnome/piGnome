#Methods associatted with databases#
import serial
import sqlite3
#connect to the local database#
myDatabase = sqlite3.connect("myDBfile.sqlite3", check_same_thread=False)
cur = myDatabase.cursor()
#initialize database#
def init_data_db(cur):
	cur.execute('''CREATE TABLE IF NOT EXISTS pGnome (RecordId INTEGER PRIMARY KEY, MoistureLevel INTEGER, GnomeZone INTEGER, CollectedTime TEXT)''')
def init_setting_db(cur):
	cur.execute('''CREATE TABLE IF NOT EXISTS levelSet (LevelId INTEGER PRIMARY KEY, MoistureLevel INTEGER, SettingTime TEXT, GnomeZone INTEGER)''')
def init_tables():
	init_data_db(cur)
	init_setting_db(cur)

#inserting data from moisture sensors#
def insert_db(cur, MoistureLevel, GnomeZone):
	cur.execute('''INSERT INTO pGnome
		(RecordId, MoistureLevel, GnomeZone, CollectedTime)
		VALUES (NULL,?,?,?)''', (MoistureLevel, GnomeZone, datetime.now()))
#main method to collect current mositure level data#
def data_collect(identifier, txt=''):
	#xbee input
	serialport = serial.Serial("/dev/ttyAMA0", 9600, timeout=5.5)
	response = serialport.read(size=26)
  	if response.__len__() > 0:
		#parse channel number and moisture data from the packet
		channel = math.log(ord(response[11]),2)
		data = ord(response[13]) * 256 + ord(response[14]) + 1
		level = int(data*100/1024)
		insert_db(cur, level, channel)

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
	for GnomeZone in range (1,4):
		recentSet = MoistureSetting.Query.filter(gnomeZone=GnomeZone).order_by("-createdAt")
		recentOne = recentSet.limit(1)
		for ob in recentOne:
			if row_count(cur,GnomeZone)[0] == 0:
				insert_setting_db(cur,ob.level,ob.createdAt,ob.gnomeZone)
			else:
				update_setting_db(cur,ob.level,ob.createdAt,ob.gnomeZone)

#pushing data from local database to parse database#
def update_remote_db(identifier,txt=''):
	cur.execute('''SELECT *
		FROM pGnome
		''')
	for record in cur.fetchall():
		gnomeScore = Moisture(level=record[1], gnomeZone=int(record[2]), collectedTime=record[3])
		gnomeScore.save()
