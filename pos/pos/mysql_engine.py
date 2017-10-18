#!/apps/python_3.5/bin/python3
# -*- coding: utf-8 -*-
"""Remove and create a dev database.

Contains dev engine.
Main will remove test db and create new one with any updates in models.py
"""

import errno
import os
from contextlib import contextmanager


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from models import BASE


__author__ = 'Brett R. Ward'

# Constants
DB_NAME = 'WoF.db'

# Create ENGINE
ENGINE = create_engine('mysql+mysqldb://{}:{}@{}:{}/{}'.format(
    'neqel',
    'jessa123',
    'localhost',
    '3306',
    'wofweb'))

# Create SESSION
SESSION = sessionmaker(bind=ENGINE)


@contextmanager
def session_scope():
    """Provide a transactional scope for a series of database interactions.

    Used to automatically handle commit errors and rollback changes.
    """
    session = SESSION()
    try:
        yield session
        session.commit()
    except Exception as exc:
        print(exc)
        session.rollback()
        raise exc
    finally:
        session.close()
