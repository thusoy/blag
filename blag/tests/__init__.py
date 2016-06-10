from .. import create_app, db
from ..auth.models import User

from flask import session
from flask_login import login_user
from functools import wraps
from nose.tools import nottest
import unittest
import os
import sys
import tempfile

PY3 = sys.version_info > (3, 0, 0)


def ignore(*exceptions):
    """ Use as decorator when you want to ignore certain exceptions.

    Example:

        @ignore(OSError)
        def sketchy():
            os.remove('does_this_exists.txt')
    """

    def wrapper(func):

        @wraps(func)
        def inner(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except exceptions:
                pass
        return inner
    return wrapper


class HTTPTestMixin(unittest.TestCase):
    """ Test mixin that proves assert200, assert201, etc helpers. """

    def _assert_response_factory(self, status_code):
        def _assert_response(response):
            self.assertEqual(response.status_code, status_code)
            data = response.data
            if PY3:
                return data.decode('utf-8')
            else:
                return data
        return _assert_response


    def __init__(self, *args, **kwargs):
        super(HTTPTestMixin, self).__init__(*args, **kwargs)
        for i in (200, 201, 204, 301, 302, 400, 401, 403, 404):
            setattr(self, 'assert%d' % i, self._assert_response_factory(i))


class UserTestCase(unittest.TestCase):
    """ Test case with a temp db and three users available: admin_user, anon_user and auth_user,
    representing unauthenticated users, like random passerbys, authenticated users, which have
    authenticated with Facebook, but nothing more, and admin users, which is basically me.

    More user types might be added later.
    """

    @nottest
    def create_test_client(self, user):
        """ Create a test client with the permissions and an active session of the given user. """
        with self.app.test_request_context():
            db.session.add(user)
            db.session.commit()

            # Login the user and save the session
            login_user(user)
            session_copy = session.copy()

        # Re-create the session with a new test client
        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                for k, v in session_copy.items():
                    sess[k] = v
            return c


    def pre_set_up(self):
        self.test_db = tempfile.NamedTemporaryFile(delete=False)
        self.test_db.close()
        self.app = create_app(SQLALCHEMY_DATABASE_URI='sqlite:///' + self.test_db.name,
            WTF_CSRF_ENABLED=False, SECRET_KEY='bogus')
        with self.app.app_context():
            db.create_all()
        self.admin_user = self.create_test_client(User(first_name='Bob', last_name='Admin', is_admin=True))
        self.anon_user = self.app.test_client()
        self.auth_user = self.create_test_client(User(first_name='Alice', last_name='User'))


    def __call__(self, *args, **kwargs):
        self.pre_set_up()
        super(UserTestCase, self).__call__(*args, **kwargs)
        self.post_tear_down()


    @ignore(OSError)
    def post_tear_down(self):
        os.remove(self.test_db.name)
