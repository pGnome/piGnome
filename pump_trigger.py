import sqlite3

db = sqlite3.connect("myDBfile.sqlite3")


def pump_sig():
	cur.execute('''SELECT MoistureLevel
		FROM levelSet
		ORDER BY SettingTime DESC
		LIMIT 1
		''')
	setting = cur.fetchone()

	cur.execute('''SELECT MoistureLevel
		FROM pGnome
		GROUP BY GnomeZone
		ORDER BY CollectedTime DESC
		''')
	readings = cur.fetchall()

	for reading in readings:
		print reading
		if setting[0] <= reading[0]:
			print 0
		else:
			print 1


cur = db.cursor()

db.commit()
pump_sig()
db.close()
