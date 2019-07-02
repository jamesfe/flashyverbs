import json
from tornado.testing import AsyncHTTPTestCase

from flashserver.flashserver import FlashServer
from flashserver.database import test_session_factory


class BasicBusinessHandlersTests(AsyncHTTPTestCase):

    def get_app(self):
        return FlashServer(ioloop=self.io_loop, settings_override={'autoreload': False}, test=True)

    def test_get_question_from_list(self):
        """Test that querying the question_list handler gets a question."""
        # TODO: Make this question getting more stable (query the db)
        url = '/list/1/'
        session = test_session_factory()

        get_res = self.fetch(url, method='GET')
        self.assertEqual(get_res.code, 200)
        list_get = json.loads(get_res.body.decode('utf-8'))
        self.assertIsInstance(list_get, dict)
        self.assertEqual({}, list_get)
