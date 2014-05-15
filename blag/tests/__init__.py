from .. import create_app, db
from ..auth.models import User

from flask import session
from flask.ext.login import login_user
from functools import wraps
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


class HTTPTestHelper(unittest.TestCase):

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
        super(HTTPTestHelper, self).__init__(*args, **kwargs)
        for i in (200, 201, 204, 301, 302, 400, 401, 403, 404):
            setattr(self, 'assert%d' % i, self._assert_response_factory(i))


class UserTestCase(HTTPTestHelper):

    def create_session(self, user):
        with self.app.test_request_context():
            db.session.add(user)
            db.session.commit()

            # Login the user and save the session
            login_user(user)
            session_copy = {k: v for k, v in session.items()}

        # Re-create the session with a new test client
        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                for k, v in session_copy.items():
                    sess[k] = v
            return c


    def preSetUp(self):
        self.test_db = tempfile.NamedTemporaryFile(delete=False)
        self.test_db.close()
        self.app = create_app(SQLALCHEMY_DATABASE_URI='sqlite:///' + self.test_db.name,
            WTF_CSRF_ENABLED=False, SECRET_KEY='bogus')
        self.admin_user = self.create_session(User(first_name='Bob', last_name='Admin', is_admin=True))
        self.anon_user = self.app.test_client()
        self.auth_user = self.create_session(User(first_name='Alice', last_name='User'))


    def __call__(self, *args, **kwargs):
        self.preSetUp()
        super(UserTestCase, self).__call__(*args, **kwargs)
        self.postTearDown()


    @ignore(OSError)
    def postTearDown(self):
        os.remove(self.test_db.name)

