import tornado.ioloop
import tornado.web
import urllib2
import json
from tornado.web import HTTPError

def WeatherAPIService(longitude, latitude):
	try:
		# print("&&&&&&&&&&&")
		weatherdata = urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&APPID=6f5d54dee41c7245df515fd94c8b8c16'.format(latitude,longitude));
		# print(weatherdata)
		# print("&&^^^^^^^^^^^^^^^^^^")
		weather_string = weatherdata.read()
		print(weather_string)
		weather_dict = json.loads(weather_string)
		# print(weather_dict)
		weather = weather_dict["weather"]
		if(weather[0].get("main")) == "Rain":
			result = "need to carry umbrella"
		else:
			result = "no need umbrella"

		return result
	except Exception as e:
		raise HTTPError(500)