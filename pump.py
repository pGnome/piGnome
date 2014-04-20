#multi-zone pump triggering#
import sqlite3
import RPi.GPIO as GPIO
import globalVals

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
			
			zoneArray = []

			for setting in settings:
				zoneArray.append(setting[0])

			globalVals.pumpOn = False
			for i in range(1, 4):
				if i in zoneArray:
					GPIO.output(gpio_pins[i], GPIO.LOW)
					globalVals.pumpOn = True
					print "watering zone "
					print i
				else:
					GPIO.output(gpio_pins[i], GPIO.HIGH)

			if globalVals.pumpOn:
				GPIO.output(gpio_pins[0], GPIO.HIGH)
				print "turning pump on"
			else:
				GPIO.output(gpio_pins[0], GPIO.LOW)
				print "turning pump off"

			break
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