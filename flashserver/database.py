# -*- coding: utf-8 -*-
"""Assets Database utilities."""

from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from flashserver.models import Base
from flashserver.utils import get_db_secrets, get_test_db_secrets


ECHO = False


def default_engine(config):
    """Return the default sqlalchemy database engine.json."""
    url = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'
    engine = create_engine(url.format(**config), echo=ECHO)
    if not database_exists(engine.url):
        try:
            create_database(engine.url)
        except IntegrityError:
            return engine  # db has already been created
    return engine


def create_tables(engine):
    Base.metadata.create_all(engine)


database = get_db_secrets()
engine = default_engine(database)
session_factory = sessionmaker(autoflush=True, autocommit=False, bind=engine)

test_database = get_test_db_secrets()
test_engine = default_engine(test_database)
test_session_factory = sessionmaker(autoflush=True, autocommit=False, bind=test_engine)

create_tables(engine)
create_tables(test_engine)
# How to use it:
# session = scoped_session(session_factory)
