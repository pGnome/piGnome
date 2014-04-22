#scheduling module

import time
from datetime import timedelta
from datetime import datetime
import weather
import globalVals

def isTime():
	currentDate = time.strftime("%A")
	scheduleTime = weather.getTodayScheduleTime(currentDate)
	if scheduleTime != "":
		half_duration = globalVals.watering_duration/2
		timeIntervalLeft = datetime.now() - timedelta(hours=4) - timedelta(minutes=half_duration)
		timeIntervalRight = timeIntervalLeft + timedelta(minutes=globalVals.watering_duration)
		if timeIntervalLeft.strftime("%X") < scheduleTime and scheduleTime < timeIntervalRight.strftime("%X"):
			print "time to water"
			return True
	print "is not the time"
	return False
