from .. import create_app, db
from ..models import BlogPost
from ..auth.models import User

from flask import session
from flask.ext.login import login_user
import json
import tempfile
import unittest


class UserTestCase(unittest.TestCase):

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


    def postTearDown(self):
        pass


class BlogTest(unittest.TestCase):

    def setUp(self):
        self.test_db = tempfile.NamedTemporaryFile(delete=False)
        self.test_db.close()
        self.app = create_app(SQLALCHEMY_DATABASE_URI='sqlite:///' + self.test_db.name,
            WTF_CSRF_ENABLED=False, SECRET_KEY='bogus')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.session.add(BlogPost(title='Test article', rendered_content='Snip', raw_content='Snip'))
            db.session.commit()
            self.post_id = BlogPost.query.first().id


    def test_main_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Test article' in response.data)
        self.assertTrue('Snip' in response.data)


    def test_post_details(self):
        response = self.client.get('/blag/%d' % self.post_id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Test article' in response.data)
        self.assertTrue('Snip' in response.data)


class WritePostTest(UserTestCase):

    def test_write_post(self):
        contents = {
            'title': 'Test article',
            'raw_content': json.dumps({'data': [{'type': 'text', 'data': {'text': 'Something'}}]}),
        }
        response = self.admin_user.post('/blog', data=contents)
        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            blogposts = BlogPost.query.all()
            self.assertEqual(len(blogposts), 1)


    def test_write_restricted(self):
        response = self.anon_user.post('/blog')
        self.assertEqual(response.status_code, 401)
        response = self.auth_user.post('/blog')
        self.assertEqual(response.status_code, 403)
