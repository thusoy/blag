from .. import db

from flask.ext.login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    fb_id = db.Column(db.String(255), unique=True)
    is_admin = db.Column(db.Boolean(), default=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
