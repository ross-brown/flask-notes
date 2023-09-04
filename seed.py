# noinspection PyUnresolvedReferences
from app import app
from models import db, User, Note


db.drop_all()
db.create_all()


user1 = User.register(
    username='michaelg',
    password='password1',
    email='user1email@gmail.com',
    first_name='Michael',
    last_name='G'
)

user2 = User.register(
    username='rossb',
    password='password2',
    email='user2email@gmail.com',
    first_name='Ross',
    last_name='B'
)


note1 = Note(
        title="michael thoughts",
        content="Some off topic thoughts are here",
        owner_username="michaelg")

note2 = Note(
        title="ross thoughts",
        content="flask has a lot of copy/paste",
        owner_username="rossb")


db.session.add_all([user1, user2])
db.session.add_all([note1, note2])
db.session.commit()
