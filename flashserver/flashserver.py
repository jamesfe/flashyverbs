import sys
import logging

import coloredlogs
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from os import path

from flashserver.database import session_factory, test_session_factory

from flashserver.handlers.business import QuestionHandler


logger = logging.getLogger('flashserver')
logger.setLevel(logging.DEBUG)
coloredlogs.install(format='%(asctime)s,%(msecs)03d - %(levelname)s: %(message)s', level='DEBUG', logger=logger, milliseconds=False)


class FlashServer(Application):

    def __init__(self, ioloop=None, settings_override: dict = {}, test: bool = False):
        if not test:
            self.session = session_factory()
        else:
            self.session = test_session_factory()
        settings = {
            'static_path': path.join(path.dirname(__file__), 'static'),
            'debug': True,
            'autoreload': True
        }
        settings.update(settings_override)

        urls = [
            (r'/question/(?P<q_id>\w+)/?', QuestionHandler)
            # (r'/', ListItems),
        ]
        super(FlashServer, self).__init__(urls, **settings)


def main():
    app = FlashServer()

    try:
        logger.info('starting flashserver app')
        http_server = HTTPServer(app)
        http_server.listen(8891, address='127.0.0.1')
        IOLoop.current().start()
    except (SystemExit, KeyboardInterrupt):
        pass

    http_server.stop()

    IOLoop.current().stop()
    sys.exit(0)


if __name__ == '__main__':
    main()
