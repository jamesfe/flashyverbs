import logging
import coloredlogs
from collections import defaultdict
from flashserver.handlers.generic import GenericHandler
from flashserver.models import PracticeQuestion, Language, Subject, VerbData, TenseGroup

logger = logging.getLogger('flashserver')
logger.propagate = False
coloredlogs.install(format='%(asctime)s,%(msecs)03d - %(levelname)s: %(message)s', level='DEBUG', logger=logger, milliseconds=False)


class VerbManager(GenericHandler):

    def get(self):
        """Provide a template listing all the questions in the database, so we can change and update them."""

        session = self.application.session
        questions = session.query(PracticeQuestion).order_by(PracticeQuestion.verb_id.asc()).all()
        languages = session.query(Language).all()
        subjs = session.query(Subject).all()
        verbdata = session.query(VerbData).order_by(VerbData.name.asc()).all()
        tenses = session.query(TenseGroup).all()

        self.render('admin_template.html',
            questions=questions,
            languages=languages,
            subjects=subjs,
            verbs=verbdata,
            tenses=tenses)

    def post(self):
        """Update the database with this info."""
        session = self.application.session

        q_updates = defaultdict(dict)
        for key, val in self.request.arguments.items():
            q_id = key.split('_')[-1]
            if type(val) is list:
                val = val[0]
            try:
                value = int(val)
            except:
                value = val.decode('utf-8').strip()
            db_key = '_'.join(key.split('_')[:-1])
            q_updates[q_id].update({db_key: value})

        new_insert = q_updates.get('new', {})
        del q_updates['new']

        questions = session.query(PracticeQuestion).all()
        for q_item in questions:
            if str(q_item.id) in q_updates:
                changed = False
                new_item = q_updates[str(q_item.id)]
                for k, v in new_item.items():
                    if getattr(q_item, k) != v:
                        logger.info('Changing {}, {}'.format(k, v))
                        setattr(q_item, k, v)
                        changed = True
                if changed:
                    logger.info('Changing {}'.format(new_item))
                    session.commit()

        if len(new_insert['question_text']) > 0 and len(new_insert['answer_text']) > 0:
            session.add(PracticeQuestion(**new_insert))
            session.commit()

        self.writejson(dict(q_updates))
