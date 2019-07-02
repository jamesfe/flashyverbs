import json
from tornado.testing import AsyncHTTPTestCase

from flashserver.flashserver import FlashServer
from flashserver.database import test_session_factory
from flashserver.models import AnswerLog

class BasicBusinessHandlersTests(AsyncHTTPTestCase):

    def get_app(self):
        return FlashServer(ioloop=self.io_loop, settings_override={'autoreload': False}, test=True)

    def test_get_question_from_list(self):
        """Test that querying the question_list handler gets a question."""
        # TODO: Make this question getting more stable (query the db)
        url = '/list/1/'

        get_res = self.fetch(url, method='GET')
        self.assertEqual(get_res.code, 200)
        list_get = json.loads(get_res.body.decode('utf-8'))
        self.assertIsInstance(list_get, dict)
        self.assertTrue('q_id' in list_get)
        self.assertTrue('a' in list_get)

    def test_post_answer_for_question(self):
        """Test that when we post a bad answer, it is checked and properly recorded."""
        url = '/list/1/'
        payload = json.dumps({
            'q_id': 2,
            'answer': 'blah'
        })

        session = test_session_factory()
        prev_answers = session.query(AnswerLog).count()

        result = self.fetch(url, method='POST', body=payload)
        body = json.loads(result.body)
        self.assertFalse(body['correct'])
        self.assertEqual(prev_answers + 1, session.query(AnswerLog).count())
