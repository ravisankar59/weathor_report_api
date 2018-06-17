from tornado import httpserver
from tornado import gen
from tornado.ioloop import IOLoop
import tornado.web
import urllib2
import json
from urls import url_patterns

class Application(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, url_patterns)

def main():

    app = Application()
    app.listen(8888)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()