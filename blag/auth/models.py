from flask_login import UserMixin
from wtforms import TextField, PasswordField

from ..models import _PrintableForm
from .. import db, porridge


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    is_admin = db.Column(db.Boolean(), default=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    def __init__(self, password=None, **kwargs):
        if password:
            kwargs['password_hash'] = porridge.boil(password)
        super(User, self).__init__(**kwargs)


    def set_password_hash(self, password):
        self.password_hash = porridge.boil(password)


    def valid_password(self, password):
        valid = porridge.verify(password, self.password_hash)
        if valid and porridge.needs_update(self.password_hash):
            self.password_hash = porridge.boil(password)
        return valid


    def __str__(self):
        return 'User(%s %s, is_admin=%s)' % (self.first_name, self.last_name, self.is_admin)


class LoginForm(_PrintableForm):
    email = TextField('Email')
    password = PasswordField('Password')
