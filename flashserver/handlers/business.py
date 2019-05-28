import logging

import coloredlogs

from flashserver.handlers.generic import GenericHandler

logger = logging.getLogger('flashserver')
logger.propagate = False
coloredlogs.install(format='%(asctime)s,%(msecs)03d - %(levelname)s: %(message)s', level='DEBUG', logger=logger, milliseconds=False)


class QuestionHandler(GenericHandler):

    def get(self, q_id):
        self.writejson({'q_id': q_id})


class ListHandler(GenericHandler):

    def get(self, list_id):
        # TODO: FIX
        practice_questions = self.session.query(
            PracticeQuestion).filter(
            VerbToList.practice_list_id == list_id,
            VerbToList.group_id == PracticeQuestion.group_

        acceptable_verbs = self.session.query(
            VerbToList.group_id, 
            VerbToList.tense_id).filter(
            VerbToList.practice_list_id == list_id).all()
        
        self.session.query(
