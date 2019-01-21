import logging

import coloredlogs
from tornado import escape

from flashserver.handlers.generic import GenericHandler
from flashserver.models import User

logger = logging.getLogger('flashserver')
logger.propagate = False
coloredlogs.install(format='%(asctime)s,%(msecs)03d - %(levelname)s: %(message)s', level='DEBUG', logger=logger, milliseconds=False)


class BuyAsset(GenericHandler):

    def post(self):
        args = escape.json_decode(self.request.body)
        username = args.get('user', None).lower()
        password_hash = args.get('password_hash', None)

        if None in [username, password_hash]:
            self.error('missing user or password', code=401)

        session = self.application.session
        existing = session.query(User.id).filter(User.username == username).first()
        if existing is not None:
            self.error('username already chosen', code=400)

        new_user = {
            'username': username,
            'password_hash': password_hash
        }
        try:
            session.add(User(**new_user))
            session.commit()
        except:  # noqa TODO: Fix this
            session.rollback()
            self.error('db error', code=500)
        finally:
            session.close()  # TODO: Confirm this is needed

        self.clear()
        self.set_status(200)
        self.finish({'result': 'user created'})

