import logging
import coloredlogs
from flashserver.handlers.generic import GenericHandler
from flashserver.models import PracticeQuestion, Language, Subject, VerbData, TenseGroup

logger = logging.getLogger('flashserver')
logger.propagate = False
coloredlogs.install(format='%(asctime)s,%(msecs)03d - %(levelname)s: %(message)s', level='DEBUG', logger=logger, milliseconds=False)


class VerbManager(GenericHandler):

    def get(self):
        """Provide a template listing all the questions in the database, so we can change and update them."""

        session = self.application.session
        questions = session.query(PracticeQuestion).all()
        languages = session.query(Language).all()
        subjs = session.query(Subject).all()
        verbdata = session.query(VerbData).all()
        tenses = session.query(TenseGroup).all()

        self.render('admin_template.html',
            questions=questions,
            languages=languages,
            subjects=subjs,
            verbs=verbdata,
            tenses=tenses)
