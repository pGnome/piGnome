import forecastio
from datetime import timedelta
from datetime import datetime

api_key = "7160deca2c6bcb9e35b9bf9b6ade6675"
oneHour = timedelta(hours=1)
last_check = 

lat = 47.611
lng = -122.333



byHour = forecast.hourly()
print byHour.summary
print "---------------------"
print byHour.icon
print "---------------------"
for hourlyData in byHour.data:
	#print hourlyData.time
	print hourlyData.precipProbability


def isRaining():


def forecast():
	forecast = forecastio.load_forecast(api_key, lat, lng, units="us")
	weatherData = forecast.hourly()
	if weatherData.icon == "rain":
		return True
	else:
		return False