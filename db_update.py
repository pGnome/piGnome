from parse_rest.connection import register
from parse_rest.datatypes import Object
import sqlite3

register("28PBuP52sksBKQskvbMEyny2jVhaECzQ72gyIqsI",
		 "o0AtN7gd9eQgPYBiCia202rDYNwYAYsnOcVfCfQ2")

class pGnomeTest(Object):
    pass

db = sqlite3.connect("myDBfile.sqlite3")

def update_db():
	cur.execute('''SELECT *
		FROM pGnome
		''')
	for record in cur.fetchall():
		gnomeScore = pGnomeTest(level=record[1], gnomeZone=record[2], collectedTime=record[3])
		gnomeScore.save()



cur = db.cursor()
update_db()
db.close()