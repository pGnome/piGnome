#multi-zone pump triggering#
import sqlite3
import RPi.GPIO as GPIO
import globalVals
import weather
import schedule

def pump_sig(identifier,gpio_pins):
	weather.updateManual()
	if globalVals.manual:
		if schedule.isTime() and not(globalVals.pumpOn):
			GPIO.output(gpio_pins[0], GPIO.HIGH)
			GPIO.output(gpio_pins[1], GPIO.LOW)
			GPIO.output(gpio_pins[2], GPIO.LOW)
			GPIO.output(gpio_pins[3], GPIO.LOW)
			globalVals.pumpOn = True
			print "turning pump on"
		else:
			GPIO.output(gpio_pins[0], GPIO.LOW)
			GPIO.output(gpio_pins[1], GPIO.HIGH)
			GPIO.output(gpio_pins[2], GPIO.HIGH)
			GPIO.output(gpio_pins[3], GPIO.HIGH)
			globalVals.pumpOn = False
			print "turning pump off"
	else:
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

				if globalVals.pumpOn and weather.isRaining() == False:
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