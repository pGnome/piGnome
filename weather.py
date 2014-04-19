import forecastio

api_key = "7160deca2c6bcb9e35b9bf9b6ade6675"
lat = -31.967819
lng = 115.87718

forecast = forecastio.load_forecast(api_key, lat, lng)

byHour = forecast.hourly()
print byHour.summary
print "---------------------"
print byHour.icon
print "---------------------"
for hourlyData in byHour.data:
        print hourlyData.temperature