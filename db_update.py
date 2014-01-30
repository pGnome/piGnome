from parse_rest.connection import register
from parse_rest.datatypes import Object
import sqlite3

register("66Z4aux6QXjcfTS4HqsyxXGyBpfXrrT2a6BUaXxe", 
		 "ZIJhoPJHoOIIv9ZYC0c76LJS1ZHLeCcNoRq8k3WE")

class pGnomeTest(Object):
    pass

db = sqlite3.connect("myDBfile.sqlite3")

def update_db():
	cur.execute('''SELECT * 
		FROM pGnome
		''')
	for record in cur.fetchall():
		gnomeScore = pGnomeTest(moisture_level=record[1], gnome_name=record[2], collected_time=record[3])
		gnomeScore.save()

cur = db.cursor()
update_db()
db.close()