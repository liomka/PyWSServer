import Settings

import WebSocketHandler

import json

import cyclone.web
import sys

from twisted.internet import reactor
from twisted.python import log


class Application(cyclone.web.Application):
    def __init__(self):
        handlers = [
            (r"/", cyclone.web.RedirectHandler, {"url": "http://www.liomka.io/demo"}),
            (r'/ws', WebSocketHandler.WebSocketHandler),
            (r'/api', ApiHandler),
            (r'/favicon.ico', cyclone.web.StaticFileHandler, {'path': "./"}),
        ]
        settings = {
            "WSServerUrl": "ws://pywsserver.herokuapp.com/ws",
            "template_path": Settings.TEMPLATE_PATH,
            "static_path": Settings.STATIC_PATH,
        }
        cyclone.web.Application.__init__(self, handlers, **settings)


class ApiHandler(cyclone.web.RequestHandler):
    @cyclone.web.asynchronous
    def get(self, *args):
        self.finish()
        id = self.get_argument("id")
        value = self.get_argument("value")
        data = {"id": id, "value": value}
        data = json.dumps(data)

    @cyclone.web.asynchronous
    def post(self):
        pass


if __name__ == '__main__':
    app = Application()
    log.startLogging(sys.stdout)

    reactor.listenTCP(Settings.HTTPPORT, app)
    reactor.run()
