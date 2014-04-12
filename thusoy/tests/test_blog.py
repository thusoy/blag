from .. import create_app, db
from ..models import BlogPost

import json
import tempfile
import unittest

class BlogTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.session.add(BlogPost(title='Test article', rendered_content='Snip', raw_content='Snip'))


    def test_main_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Test article' in response.data)
        self.assertTrue('Snip' in response.data)


class WritePostTest(unittest.TestCase):

    def setUp(self):
        self.test_db = tempfile.NamedTemporaryFile(delete=False)
        self.test_db.close()
        self.app = create_app(SQLALCHEMY_DATABASE_URI='sqlite:///' + self.test_db.name,
            WTF_CSRF_ENABLED=False, SECRET_KEY='bogus')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()


    def test_write_post(self):
        contents = {
            'title': 'Test article',
            'raw_content': json.dumps({'data': [{'type': 'text', 'data': {'text': 'Something'}}]}),
        }
        response = self.client.post('/blog', data=contents)
        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            blogposts = BlogPost.query.all()
            self.assertEqual(len(blogposts), 1)
