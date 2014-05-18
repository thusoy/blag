from . import UserTestCase
from .. import db
from ..models import BlogPost

import json


class BlogTest(UserTestCase):

    def setUp(self):
        with self.app.app_context():
            db.session.add(BlogPost(title='Test article', rendered_content='Snip', raw_content='Snip'))
            db.session.commit()
            self.post_id = BlogPost.query.first().id


    def test_main_page(self):
        response = self.anon_user.get('/')
        data = self.assert200(response)
        self.assertTrue('Test article' in data)
        self.assertTrue('Snip' in data)


    def test_post_details(self):
        response = self.anon_user.get('/blag/%d' % self.post_id)
        data = self.assert200(response)
        self.assertTrue('Test article' in data)
        self.assertTrue('Snip' in data)


    def test_styleguide(self):
        response = self.anon_user.get('/styleguide')
        self.assert200(response)


class WritePostTest(UserTestCase):

    def test_get_write_form(self):
        self.assert200(self.admin_user.get('/blog'))


    def test_write_post(self):
        contents = {
            'title': 'Test article',
            'raw_content': json.dumps({'data': [{'type': 'text', 'data': {'text': 'Something'}}]}),
        }
        response = self.admin_user.post('/blog', data=contents)
        self.assert302(response)
        with self.app.app_context():
            blogposts = BlogPost.query.all()
            self.assertEqual(len(blogposts), 1)


    def test_write_restricted(self):
        self.assert401(self.anon_user.post('/blog'))
        self.assert403(self.auth_user.post('/blog'))
