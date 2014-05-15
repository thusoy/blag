from .. import db, oauth
from .models import User

from flask import Blueprint, request, session, url_for, redirect, current_app
from flask.ext.login import login_user, logout_user
from flask.ext.principal import identity_changed, Identity, AnonymousIdentity


mod = Blueprint('auth', __name__, template_folder='templates')

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key='403591906450053',
    consumer_secret='577f1c58c777f1366b80983db5b3163d',
    request_token_params={'scope': 'email'}
)


@mod.route('/login')
def login():
    return facebook.authorize(callback=url_for('.facebook_authorized',
        next='/',
        _external=True))


@mod.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    user = User.query.filter_by(fb_id=me.data.get('id')).first()
    if not user:
        user = User(fb_id=me.data.get('id'), first_name=me.data.get('first_name'),
            last_name=me.data.get('last_name'))
        db.session.add(user)
        db.session.commit()
    login_user(user)
    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
    redirect_uri = request.args.get('next')

    # Make sure we don't redirect off-site
    redirect_uri = redirect_uri if redirect_uri[0] == '/' else '/'
    return redirect(redirect_uri)


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


@mod.route('/logout')
def logout():
    logout_user()
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    return redirect('/')
