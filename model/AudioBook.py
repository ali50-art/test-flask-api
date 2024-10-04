import uuid
import datetime
from .Votes import Vote
from model import app, db, bcrypt
class Audiobook(db.Model):
    __tablename__ = "audiobooks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    published_on = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    cover_image_url = db.Column(db.String, nullable=True)  # Cover image URL

    def __init__(self, title, author, description, cover_image_url):
        self.title = title
        self.author = author
        self.published_on = datetime.datetime.now()
        self.description = description
        self.cover_image_url = cover_image_url

    def get_vote_count(self):
        return Vote.query.filter_by(audiobook_id=self.id).count()