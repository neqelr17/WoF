#!/apps/python_3.5/bin/python3
# -*- coding: utf-8 -*-
"""Remove and create a dev database.

Contains dev engine.
Main will remove test db and create new one with any updates in models.py
"""

import errno
import json
import os
import sys
from contextlib import contextmanager
from datetime import datetime


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from filetracker.models import (BASE,
                                User,
                                ClientApplication,
                                Listener,
                                Order,
                                File,
                                PivotFile)


__author__ = 'Brett R. Ward'

# Constants
DB_NAME = 'file_tracker.db'
TEST_DATA = 'test_data.json'
TEST_DIR = 'tests/'
DATETIME_STR_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

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

    # Open up test data json and load data to database.
    with session_scope() as session:
        print('Inserting test data.')
        insert_test_data(session, '{}{}'.format(TEST_DIR, '{}{}'.format(
            TEST_DIR, TEST_DATA)))
    print('Success!')


def insert_test_data(session, test_data):
    """Insert Data into test database."""
    with open(test_data, 'r') as fh_users:
        data = json.load(fh_users)
        add_users(data, session)
        import_apps(data, session)
        add_listeners(data, session)
        add_orders(data, session)
        add_files(data, session)
        add_pivot_files(data, session)


def add_users(data, session):
    """Add users from json file.

    Used for development to import test data to database.
    """
    for user in data['users']:
        session.add(User(
            user_name=user['user_name'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            email=user['email']
        ))
    session.commit()


def import_apps(data, session):
    """Add users from json file.

    Used for development to import test data to database.
    """
    for app in data['client_apps']:
        session.add(ClientApplication(
            client_code=app['client_code'],
            project_code=app['project_code'],
            days_to_keep=app['days_to_keep'],
            run_process_time=app['run_process_time'],
            pivot_track_time=app['pivot_track_time'],
            pivot_archive_time=app['pivot_archive_time'],
            pivot_audit_time=app['pivot_audit_time'],
            created_user_id=app['created_user_id'],
            last_modified_user_id=app['last_modified_user_id'],
            created=datetime.utcnow(),
            last_modified=datetime.utcnow()
        ))
    session.commit()


def add_listeners(data, session):
    """Add users from json file.

    Used for development to import test data to database.
    """
    for listner in data['listeners']:
        temp = Listener()
        temp.app = session.query(ClientApplication).filter_by(
            id=int(listner['app_id'])).first()
        temp.user = session.query(User).filter_by(
            id=int(listner['user_id'])).first()
        session.add(temp)
    session.commit()


def add_orders(data, session):
    """Add orders from test_data.json.

    Used for develpment and testing.
    """
    for order in data['orders']:
        temp = Order()
        temp.app = session.query(ClientApplication).filter_by(
            id=order['app_id']).first()
        temp.sales_code = order['sales_code']
        temp.order_number = order['order_number']
        temp.sales_code = order['sales_code']
        temp.four_year_location = order['four_year_location']
        temp.run_start = datetime.strptime(order['start'], DATETIME_STR_FORMAT)
        session.add(temp)
    session.commit()


def add_files(data, session):
    """Add files from test_data.json.

    Used for develpment and testing.
    """
    for i_file in data['files']:
        temp = File(
            name=i_file['name'],
            file_type=i_file['file_type'],
            received=datetime.strptime(i_file['received'], DATETIME_STR_FORMAT)
            )
        temp.app = session.query(ClientApplication).filter_by(
            id=i_file['app_id']).first()
        temp.order = session.query(Order).filter_by(
            id=i_file['order_id']).first()
        try:
            temp.sha = File.hash_file('{}{}'.format(TEST_DIR, i_file['name']))
        except FileNotFoundError:
            print('Could not find file to compute sha hash.')
        session.add(temp)
    session.commit()


def add_pivot_files(data, session):
    """Add pivot files from test_data.json.

    Used for develpment and testing.
    """
    for p_file in data['pivot_files']:
        temp = PivotFile()
        temp.order = session.query(Order).filter_by(
            id=p_file['order_id']).first()
        temp.pivot_type = p_file['pivot_type']
        temp.name = p_file['name']
        temp.sent = datetime.strptime(
            p_file['sent'], DATETIME_STR_FORMAT)
        session.add(temp)
    session.commit()


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
