import os

os.environ["DATABASE_URL"] = 'postgresql:///notes_test'

from unittest import TestCase

from app import app
from models import db, User, Note

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

AUTH_KEY = "username"

db.drop_all()
db.create_all()



test_user = User.register(
    username='test_user',
    password='password',
    email='user2email@gmail.com',
    first_name='Ross',
    last_name='B'
)


test_note = Note(
        title="test title",
        content="test content",
        owner_username="test_user")


class NotesViewsTestCase(TestCase):
    """Test for views of notes app"""
    def setUp(self):
        user = test_user
        db.session.add_all([test_user, test_note])
        db.session.commit()

        self.username = user.username
        session[AUTH_KEY] = self.username

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()