from parse_rest.connection import register
from parse_rest.datatypes import Object
import sqlite3

register("66Z4aux6QXjcfTS4HqsyxXGyBpfXrrT2a6BUaXxe", 
		 "ZIJhoPJHoOIIv9ZYC0c76LJS1ZHLeCcNoRq8k3WE")

class pGnomeTest(Object):
    pass

class MoistureSetting(Object):
    pass

db = sqlite3.connect("myDBfile.sqlite3")

def init_setting_db(cur):
	cur.execute('''CREATE TABLE IF NOT EXIST levelSet
		(LevelId INTEGER PRIMARY KEY,

def update_db(cur):
	cur.execute('''SELECT * 
		FROM pGnome
		''')
	for record in cur.fetchall():
		gnomeScore = pGnomeTest(level=record[1], gnomeZone=record[2], collectedTime=record[3])
		gnomeScore.save()

cur = db.cursor()
update_db()
db.close()
