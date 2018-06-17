import tornado.ioloop
import tornado.web
import urllib2
import json
from services import WeatherAPIService

class MainHandler(tornado.web.RequestHandler):
    def post(self):
    	data = json.loads(self.request.body)
    	longitude = data.get('longitude')
    	latitude = data.get('latitude')
        response = WeatherAPIService(longitude, latitude)
        self.write(json.dumps(dict(response=response)))