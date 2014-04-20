#weather module
from parse_rest.connection import register
from parse_rest.datatypes import Object
import forecastio

#connect to the parse database#
register("28PBuP52sksBKQskvbMEyny2jVhaECzQ72gyIqsI",
         "ZVYfNMONIiMD9XLEhhUKJqZh4tuHNBRiFPCLnx25")

api_key = "7160deca2c6bcb9e35b9bf9b6ade6675"

#location table
class Location(Object):
    pass

#check if the current location is raining
def isRaining():
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
