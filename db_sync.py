from parse_rest.connection import register
from parse_rest.datatypes import Object
import sqlite3
import time


register("28PBuP52sksBKQskvbMEyny2jVhaECzQ72gyIqsI",
		 "ZVYfNMONIiMD9XLEhhUKJqZh4tuHNBRiFPCLnx25")

db = sqlite3.connect("myDBfile.sqlite3")

#parse tables
#mositure history table
class Moisture(Object):
    pass

class Barrel(Object):
	pass

#pushing data from local database to parse database#
def update_remote_db(cur):
	#moisture level
	cur.execute('''SELECT *
		FROM pGnome
		''')
	for record in cur.fetchall():
		gnomeScore = Moisture(level=record[1], gnomeZone=int(record[2]), collectedTime=record[3])
		gnomeScore.save()

	#water level
	cur.execute('''SELECT *
		FROM waterLevel
		''')
	for record in cur.fetchall():
		gnomeScore = Barrel(level=record[1], collectedTime=record[2])
		gnomeScore.save()


cur = db.cursor()

while True:
	update_remote_db(cur)
	db.commit()
	time.sleep(60)

db.commit()
db.close()
