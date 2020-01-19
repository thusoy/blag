from flask import Blueprint, request, session, url_for, redirect, current_app, render_template, abort
from flask_login import login_user, logout_user
from flask_principal import identity_changed, Identity, AnonymousIdentity

from .. import db
from .models import User, LoginForm


mod = Blueprint('auth', __name__, template_folder='templates')

@mod.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not user.valid_password(form.password.data):
            abort(401)

        login_user(user)
        return redirect('/')
    return render_template('login.html', login_form=form)


@mod.route('/logout')
def logout():
    logout_user()
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    return redirect('/')
