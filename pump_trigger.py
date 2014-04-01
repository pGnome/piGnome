import RPi.GPIO as GPIO
import sqlite3
import time

db = sqlite3.connect("myDBfile.sqlite3")
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
#pump GPIO pin
GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)
#zone GPIO pins
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)

def pump_sig(cur):
	cur.execute('''SELECT gnomeRecords.GnomeZone
		FROM (SELECT MoistureLevel, GnomeZone, MAX(RecordId) as gnomeId
			  FROM pGnome
			  GROUP BY GnomeZone) as gnomeRecords, levelSet
		WHERE gnomeRecords.GnomeZone = levelSet.GnomeZone AND
			  gnomeRecords.MoistureLevel < levelSet.MoistureLevel
		''')
	settings = cur.fetchall()
	

	for setting in settings:
		GPIO.output(12, GPIO.HIGH)
		if setting == 1:
			GPIO.output(11, GPIO.HIGH)
		elif setting == 2:
			GPIO.output(13, GPIO.HIGH)
		elif setting == 3:
			GPIO.output(15, GPIO.HIGH)
cur = db.cursor()
while True:
	pump_sig(cur)
	time.sleep(1)
	
GPIO.cleanup()
db.close()
