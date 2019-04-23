import logging
import random

import coloredlogs

from flashserver.handlers.generic import GenericHandler
from flashserver.database import session_factory
from flashserver.models import PracticeQuestion


logger = logging.getLogger('flashserver')
logger.propagate = False
coloredlogs.install(format='%(asctime)s,%(msecs)03d - %(levelname)s: %(message)s', level='DEBUG', logger=logger, milliseconds=False)
session = session_factory()


class QuestionHandler(GenericHandler):

    def get_question_type():
        rand_num = random.rand()
        learned_cutoff = 0.9
        unlearned_cutoff = 0.5
        if rand_num >= learned_cutoff:
            return 'learned'
        if rand_num >= unlearned_cutoff:
            return 'unlearned'
        else:
            return 'in_progress'

    def get(self, q_id):
        # question_type = get_question_type()
        res = session.query(PracticeQuestion.question_text).filter(PracticeQuestion.id == q_id).first()
        ret_val = {}
        if res is not None:
            ret_val = {
                'status': 'success',
                'q_id': q_id,
                'question': res.question_text
            }
        else:
            ret_val = {
                'status': 'error',
                'message': 'this qid not found'
            }
        self.writejson(ret_val)
