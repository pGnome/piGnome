import RPi.GPIO as GPIO
import sqlite3

db = sqlite3.connect("myDBfile.sqlite3")
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

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
			GPIO.output(12, GPIO.LOW)
		else:
			GPIO.output(12, GPIO.HIGH)
		

cur = db.cursor()
while True:
	pump_sig()
	
GPIO.cleanup()
db.close()
	