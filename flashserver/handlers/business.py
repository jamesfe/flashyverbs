import logging

import coloredlogs

from flashserver.handlers.generic import GenericHandler

logger = logging.getLogger('flashserver')
logger.propagate = False
coloredlogs.install(format='%(asctime)s,%(msecs)03d - %(levelname)s: %(message)s', level='DEBUG', logger=logger, milliseconds=False)


class QuestionHandler(GenericHandler):

    def get(self, q_id):
        self.writejson({'q_id': q_id})
