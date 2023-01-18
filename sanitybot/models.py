from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(25))
    middlename = db.Column(db.String(25))
    lastname = db.Column(db.String(25))
    address = db.Column(db.String(50))
    contact = db.Column(db.String(15))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(100))
    is_assess = db.Column(db.Boolean, default=False, nullable=False)
    epds_score = db.Column(db.Integer)
    date_submitted = db.Column(db.Date)


class User_health(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(25))
    middlename = db.Column(db.String(25))
    lastname = db.Column(db.String(25))
    address = db.Column(db.String(50))
    contact = db.Column(db.String(15))
    date_submitted = db.Column(db.Date)
    condition = db.Column(db.String(50))
    state = db.Column(db.String(25))


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(100))

class ChatHistory(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(1000))
