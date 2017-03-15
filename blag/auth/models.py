from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error
from flask_login import UserMixin
from wtforms import TextField, PasswordField

from ..models import _PrintableForm
from .. import db

password_hasher = PasswordHasher()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    is_admin = db.Column(db.Boolean(), default=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    def __init__(self, password=None, **kwargs):
        if password:
            kwargs['password_hash'] = password_hasher.hash(password)
        super(User, self).__init__(**kwargs)


    def set_password_hash(self, password):
        self.password_hash = password_hasher.hash(password)


    def valid_password(self, password):
        try:
            password_hasher.verify(self.password_hash, password)
        except Argon2Error:
            return False
        else:
            return True


    def __str__(self):
        return 'User(%s %s, is_admin=%s)' % (self.first_name, self.last_name, self.is_admin)


class LoginForm(_PrintableForm):
    email = TextField('Email')
    password = PasswordField('Password')
