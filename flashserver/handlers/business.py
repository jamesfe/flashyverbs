import logging
import json

import coloredlogs

from flashserver.handlers.generic import GenericHandler
from flashserver.models import VerbToList, VerbData, PracticeQuestion, AnswerLog

logger = logging.getLogger('flashserver')
logger.propagate = False
coloredlogs.install(format='%(asctime)s,%(msecs)03d - %(levelname)s: %(message)s', level='DEBUG', logger=logger, milliseconds=False)


class QuestionHandler(GenericHandler):

    def get(self, q_id):
        self.writejson({'q_id': q_id})


class ListHandler(GenericHandler):

    def get_valid_questions(self, list_id):
        """Given a list_id return all the valid questions for this list."""
        session = self.application.session
        all_list_connections = session.query(VerbToList.group_id, VerbToList.tense_id).filter(VerbToList.practice_list_id == list_id).all()
        questions = []
        for item in all_list_connections:
            valid_groups = session.query(VerbData.id).filter(VerbData.group_id == item.group_id).all()
            subquery = session.query(PracticeQuestion).filter(
                PracticeQuestion.tense_id == item.tense_id,
                PracticeQuestion.verb_id.in_(valid_groups)).all()
            questions.extend(subquery)
        return questions

    def get(self, list_id):
        """Get a question based on a list."""
        questions = self.get_valid_questions(list_id)

        if len(questions) > 0:
            q = questions[0]
            question = {
                'q': q.question_text,
                'a': q.answer_text,
                'q_id': q.id
            }
            self.writejson(question)
        else:
            self.writejson({})

    def post(self, list_id):
        """Someone will post an answer to a question to this list endpoint.  It's not intuitive
        but it gives us the user's name (insecure for now) and it associates the question with a list."""
        session = self.application.session
        payload = json.loads(self.request.body)
        answer = payload['answer'].strip().lower()
        question = session.query(PracticeQuestion).filter(PracticeQuestion.id == payload['q_id']).first()
        # TODO: what if there is no question?
        if question is None:
            self.writejson({'status': 'wrong'})
            # Probably not the best but we can change this later, it's an edge case.

        correct = answer == question.answer_text.lower()
        answer_log = {
            'question_id': payload['q_id'],
            'value_entered': payload['answer'],
            'list_id': list_id,
            'correct': correct
        }
        session.add(AnswerLog(**answer_log))
        session.commit()
        response = {'correct': correct}
        self.writejson(response)
