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
ENGINE = create_engine('sqlite:///{}'.format(DB_NAME))

# Create SESSION
SESSION = sessionmaker(bind=ENGINE)


def main():
    """Delete test sqlite db and create new one with.

    This is only for dev or testing. This just makes it easy to remove
    and create a new test db.
    """
    create_test_db(DB_NAME)


def create_test_db(db_filename):
    """Delete db if already exists and then create and load with test data."""
    remove_test_db(db_filename)

    print('Creating Tables')
    BASE.metadata.create_all(ENGINE, checkfirst=True)
    print('Success!')


def remove_test_db(filename):
    """Quietly removes the database file if it exists."""
    try:
        os.remove(filename)
    except OSError as exc:
        if exc.errno != errno.ENOENT:
            raise


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


if __name__ == "__main__":
    main()
