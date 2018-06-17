# test_async.py
import json
import unittest,urllib
from tornado.concurrent import Future
from tornado.web import HTTPError
from tornado.web import Application
from tornado.testing import gen_test
from mock import patch
from tornado.testing import AsyncHTTPTestCase
from handlers import MainHandler
from services import WeatherAPIService
from StringIO import StringIO

class TestMainHandler(AsyncHTTPTestCase):

    request_headers = {"content-type": "application/json"}
    route = "/weatherforecast"

    def get_app(self):
        return Application([('/weatherforecast', MainHandler)])

    @patch('handlers.WeatherAPIService')
    def test_weather_post_call(self, WeatherAPIService):
    	result = {"longitude":52, "latitude":35}
    	# case 1
    	expected_result = "need to carry umbrella"
    	WeatherAPIService.return_value = expected_result
    	route = "/weatherforecast"
    	response = self.fetch(route, method = "POST", body = json.dumps(result),
                            headers=self.request_headers)
    	self.assertEquals(response.code, 200)
    	response = json.loads(response.body.decode('utf-8'))
    	self.assertEquals(response["response"], expected_result)

    	#case2
    	expected_result = "no need umbrella"
    	WeatherAPIService.return_value = expected_result
    	response = self.fetch(route, method = "POST", body = json.dumps(result),
                            headers=self.request_headers)
    	response = json.loads(response.body.decode('utf-8'))
    	self.assertEquals(response["response"], expected_result)
 
    	WeatherAPIService.side_effect = HTTPError(500)
    	response = self.fetch(route, method = "POST", body = json.dumps(result),
                            headers=self.request_headers)
    	self.assertEquals(response.code, 500)

    @patch('services.urllib2')
    def test_weather_services(self, urllib2):
    	api_result = StringIO('{"weather": [{"main": "Rain"}]}')
    	urllib2.urlopen.return_value = api_result
    	result = WeatherAPIService(1,2)
    	expected_result = "need to carry umbrella"
    	self.assertEquals(result, expected_result)
    	# when weather is not Rain
    	api_result = StringIO('{"weather": [{"main": "Cloud"}]}')
    	urllib2.urlopen.return_value = api_result
    	result = WeatherAPIService(1,2)
    	expected_result = "no need umbrella"
    	self.assertEquals(result, expected_result)
    	# when it raises an Exception
    	urllib2.urlopen.side_effect = Exception()
    	with self.assertRaises(HTTPError):
    		result = WeatherAPIService(1,2)



if __name__ == '__main__':
    unittest.main()