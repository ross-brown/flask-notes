# noinspection PyUnresolvedReferences
from app import app
from models import db, User


db.drop_all()
db.create_all()


user1 = User.register(
    username='michaelg',
    password='password1',
    email='user1email@google.com',
    first_name='Michael',
    last_name='G'
)

user2 = User.register(
    username='rossb',
    password='password2',
    email='user2email@google.com',
    first_name='Ross',
    last_name='B'
)

db.session.add_all([user1, user2])
db.session.commit()
