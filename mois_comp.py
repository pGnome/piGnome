from parse_rest.connection import register
from parse_rest.datatypes import Object
import sqlite3

register("28PBuP52sksBKQskvbMEyny2jVhaECzQ72gyIqsI",
		 "ZVYfNMONIiMD9XLEhhUKJqZh4tuHNBRiFPCLnx25")

class moistureSetting(Object):
    pass

db = sqlite3.connect("myDBfile.sqlite3")

def init_db(cur):
	cur.execute('''CREATE TABLE levelSet (LevelId INTEGER PRIMARY KEY, MoistureLevel INTEGER, SettingTime TEXT)''')

def populate_db(cur, MoistureLevel, SettingTime):
	cur.execute('''INSERT INTO levelSet
		(LevelId, MoistureLevel, SettingTime)
		VALUES (NULL,?,?)''', (MoistureLevel, SettingTime))

def print_db():
	cur.execute('''SELECT *
		FROM levelSet
		''')
	print cur.fetchall()

cur = db.cursor()

recentSet = moistureSetting.Query.all().order_by("-createdAt")
recentOne = recentSet.limit(1)
for ob in recentOne:
	populate_db(cur,ob.moistureLevel,ob.createdAt)
db.commit()
print_db()
db.close()
