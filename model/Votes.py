# models/vote.py
import datetime

from model import app, db, bcrypt

class Vote(db.Model):
    __tablename__ = "votes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String, db.ForeignKey('users.username'), nullable=False)
    audiobook_id = db.Column(db.Integer, db.ForeignKey('audiobooks.id'), nullable=False)
    voted_on = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref='votes')
    audiobook = db.relationship('Audiobook', backref='votes')

    def __init__(self, user_id, audiobook_id):
        self.user_id = user_id
        self.audiobook_id = audiobook_id
        self.voted_on = datetime.datetime.now()
