import logging
import coloredlogs
from flashserver.handlers.generic import GenericHandler

logger = logging.getLogger('flashserver')
logger.propagate = False
coloredlogs.install(format='%(asctime)s,%(msecs)03d - %(levelname)s: %(message)s', level='DEBUG', logger=logger, milliseconds=False)


class VerbManager(GenericHandler):

    def get(self, list_id):
        """Provide a template listing all the questions in the database, so we can change and update them."""
        self.writejson('{}')
