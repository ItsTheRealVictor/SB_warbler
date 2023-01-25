"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database


# home computer DB 
# os.environ['DATABASE_URL'] = (os.environ.get('DATABASE_URL', 'postgresql://postgres:admin@localhost/test_warbler'))

# work computer DB
os.environ['DATABASE_URL'] = (os.environ.get('DATABASE_URL', 'sqlite:///test_warbler.db'))



# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""


    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        test_users = [
            {
                'email': 'hank@strickland.com',
                'username': 'HankHill',
                'password': 'propane',
            },
            {
                'email': 'peggy@arlenpublicschools.com',
                'username': 'PeggyHill',
                'password': 'boggle',
            },
            {
                'email': 'dale@dalesdeadbug.com',
                'username': 'DaleG',
                'password': 'bugs',
            },
        ]


        for user in test_users:
            new = User.signup(email=user['email'],
                        username=user['username'],
                        password=user['password'],
                        image_url=None)
            db.session.add(new)
            db.session.commit()
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_models(self):
        """Testing User Model basics"""

        users = User.query.all()
        for user in users:
            # Users should have no messages & no followers

            self.assertEqual(len(user.messages), 0)
            self.assertEqual(len(user.followers), 0)

    def test_bad_signup(self):
        invalid = User.signup(None, "asdf@asdf.com", "password", None)
        uid = 123456789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_no_email(self):
        bad_email = User.signup(username='JohnRedcorn',email=None,password='wematanye', image_url=None)
        uid = 69
        bad_email.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()


