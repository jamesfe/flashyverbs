import json
import logging

import coloredlogs
from tornado.web import RequestHandler

logger = logging.getLogger('flashserver')
logger.propagate = False
coloredlogs.install(format='%(asctime)s,%(msecs)03d - %(levelname)s: %(message)s', level='DEBUG', logger=logger, milliseconds=False)


class GenericHandler(RequestHandler):

    def notfound(self):
        self.clear()
        self.set_status(404)
        self.finish('not found')
        return None

    def writejson(self, thing):
        self.write(json.dumps(thing))

    def error(self, msg: str, code: int = 400):
        self.clear()
        self.set_status(code)
        self.finish(msg)


class BuyAsset(GenericHandler):

    def post(self):
        self.writejson({})
