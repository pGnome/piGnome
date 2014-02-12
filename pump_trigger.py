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
	print setting
	cur.execute('''SELECT MoistureLevel, GnomeZone
		FROM pGnome
		GROUP BY GnomeZone
		ORDER BY CollectedTime DESC
		LIMIT 1
		''')
	readings = cur.fetchall()
	print readings
	for reading in readings:
		print reading
		if setting[0] <= reading[0]:
			GPIO.output(12, GPIO.LOW)
			print "low"
		else:
			GPIO.output(12, GPIO.HIGH)
			print "high"
			time.sleep(20)
			GPIO.output(12, GPIO.LOW)
			break

cur = db.cursor()
while True:
	pump_sig(cur)
	time.sleep(5)
	
GPIO.cleanup()
db.close()
