from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user2_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class RelativeAdd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user2_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class Relatives(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    relatives = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    admin = db.Column(db.Boolean, default=False)
    relatives = db.relationship("Relatives")