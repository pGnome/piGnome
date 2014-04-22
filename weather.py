#weather module
from parse_rest.connection import register
from parse_rest.datatypes import Object
import forecastio
import globalVals

#connect to the parse database#
register("28PBuP52sksBKQskvbMEyny2jVhaECzQ72gyIqsI",
         "ZVYfNMONIiMD9XLEhhUKJqZh4tuHNBRiFPCLnx25")

api_key = "7160deca2c6bcb9e35b9bf9b6ade6675"

#location table
class Location(Object):
    pass
#schedule table
class Schedule(Object):
    pass
#manual override
class Manual(Object):
    pass

#check if the current location is raining
def isRaining():
	print "testing weather"
	lat = 0
	lng = 0
	recentSet = Location.Query.all().order_by("-createdAt")
	recentOne = recentSet.limit(1)
	for ob in recentOne:
		lat = ob.lat
		lng = ob.lon
	forecast = forecastio.load_forecast(api_key, lat, lng, units="us")
	weatherData = forecast.hourly()
	if weatherData.icon == "rain":
		return True
	else:
		return False

#method for retrieving today's watering schedule
def getTodayScheduleTime(day):
	recentSet = Schedule.Query.filter(day=day).order_by("-createdAt")
	recentOne = recentSet.limit(1)
	scheduleTime = ""
	duration = 1.0
	for ob in recentOne:
		scheduleTime = parser.parser().parse(ob.at, None).strftime("%X")
		duration = ob.duration * 60.0
	globalVals.watering_duration = duration
	return scheduleTime

#method to update if the manual override is on
def updateManual():
	recentSet = Manual.Query.all().order_by("-createdAt")
	recentOne = recentSet.limit(1)
	for ob in recentOne:
		globalVals.manual = ob.override
