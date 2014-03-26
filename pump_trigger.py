import RPi.GPIO as GPIO
import sqlite3
import time

db = sqlite3.connect("myDBfile.sqlite3")
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)

def pump_sig(cur):
	cur.execute('''SELECT MoistureLevel
		FROM levelSet
		ORDER BY SettingTime DESC
		LIMIT 1
		''')
	setting = cur.fetchone()
	cur.execute('''SELECT MoistureLevel, GnomeZone, MAX(RecordId)
		FROM pGnome
		GROUP BY GnomeZone
		''')
	readings = cur.fetchall()
	print readings
	for reading in readings:
		if setting[0] <= reading[0]:
			GPIO.output(12, GPIO.LOW)
		else:
			GPIO.output(12, GPIO.HIGH)
			break

cur = db.cursor()
while True:
	pump_sig(cur)
	time.sleep(3)
	
GPIO.cleanup()
db.close()
