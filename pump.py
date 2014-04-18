#multi-zone pump triggering#
import sqlite3
import RPi.GPIO as GPIO

def pump_sig(identifier,gpio_pins):
	unlock_db("myDBfile.sqlite3")
	#connect to the local database#
	myDatabase = sqlite3.connect("myDBfile.sqlite3", check_same_thread=False)
	cur = myDatabase.cursor()

	while True:
		try:
			cur.execute('''SELECT gnomeRecords.GnomeZone
				FROM (SELECT MoistureLevel, GnomeZone, MAX(RecordId) as gnomeId
					  FROM pGnome
					  GROUP BY GnomeZone) as gnomeRecords, levelSet
				WHERE gnomeRecords.GnomeZone = levelSet.GnomeZone AND
					  gnomeRecords.MoistureLevel < levelSet.MoistureLevel
				''')
			settings = cur.fetchall()
			

			for setting in settings:
				print setting[0]
				GPIO.output(gpio_pins[0], GPIO.HIGH)
				if setting[0] == 1:
					GPIO.output(gpio_pins[1], GPIO.LOW)
				elif setting[0] == 2:
					GPIO.output(gpio_pins[2], GPIO.LOW)
				elif setting[0] == 3:
					GPIO.output(gpio_pins[3], GPIO.LOW)

			break;
		except Exception:
			unlock_db("myDBfile.sqlite3")

	try:	
		myDatabase.commit()
		myDatabase.close()
	except Exception:
		myDatabase.rollback()

	#print identifier

def unlock_db(db_filename):
    connection = sqlite3.connect(db_filename)
    connection.commit()
    connection.close()