import json

import logging

import coloredlogs

logger = logging.getLogger('shared_utils')
logger.propagate = False
coloredlogs.install(format='%(asctime)s,%(msecs)03d - %(levelname)s: %(message)s', level='DEBUG', logger=logger, milliseconds=False)


SECRET_FILE = './secrets.json'
SECRET_CONTENTS = {}
with open(SECRET_FILE, 'r') as ifile:
    SECRET_CONTENTS = json.load(ifile)


def get_db_secrets():
    logger.info('Getting database secrets from secret file.')
    return SECRET_CONTENTS.get('db_secrets', {})


def get_test_db_secrets():
    logger.info('Getting database secrets from secret file.')
    return SECRET_CONTENTS.get('test_db_secrets', {})
