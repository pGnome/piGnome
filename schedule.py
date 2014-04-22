#scheduling module

import time
from datetime import timedelta
from datetime import datetime
import dateutil.parser as parser
import weather
import globalVals

def isTime():
	currentDate = time.strftime("%A")
	scheduleTime = db.getTodayScheduleTime(currentDate)
	if scheduleTime != "":
		half_duration = watering_duration/2
		timeIntervalLeft = datetime.now() - timedelta(minutes=half_duration)
		timeIntervalRight = timeIntervalLeft + timedelta(minutes=globalVals.watering_duration)
		if timeIntervalLeft.strftime("%X") < scheduleTime and scheduleTime < timeIntervalRight.strftime("%X"):
			return True
	return False
