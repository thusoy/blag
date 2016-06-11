from . import UserTestCase, HTTPTestMixin
from .. import db
from ..models import BlogPost

import datetime
import json


class BlogTest(UserTestCase, HTTPTestMixin):

    def setUp(self):
        with self.app.app_context():
            db.session.add(BlogPost(title='Test article', rendered_content='Snip',
                raw_content='Snip', slug='test-article',
                datetime_added=datetime.datetime(2015, 01, 01)))
            db.session.commit()
            self.post_id = BlogPost.query.first().id


    def test_main_page(self):
        response = self.anon_user.get('/')
        data = self.assert200(response)
        self.assertTrue('Test article' in data)
        self.assertTrue('Snip' in data)


    def test_post_details(self):
        response = self.anon_user.get('/2015/test-article')
        data = self.assert200(response)
        self.assertTrue('Test article' in data)
        self.assertTrue('Snip' in data)


    def test_old_redirects(self):
        response = self.anon_user.get('/blag/%d' % self.post_id)
        self.assert302(response)


    def test_post_details_404(self):
        response = self.anon_user.get('/2001/random')
        self.assert404(response)


    def test_styleguide(self):
        response = self.anon_user.get('/styleguide')
        self.assert200(response)



class MultiplePostTest(UserTestCase, HTTPTestMixin):

    def setUp(self):
        with self.app.app_context():
            db.session.add(BlogPost(title='Test 2016 article', rendered_content='Snip',
                raw_content='Snip', datetime_added=datetime.datetime(2016, 01, 01),
                slug='test-2016-article'))
            db.session.add(BlogPost(title='Test 2015 article', rendered_content='Snip',
                raw_content='Snip', datetime_added=datetime.datetime(2015, 12, 31),
                slug='test-2015-article'))
            db.session.commit()
            self.post_id = BlogPost.query.first().id


    def test_list_blank_year(self):
        response = self.anon_user.get('/2014')
        data = self.assert200(response)
        self.assertTrue('No posts found' in data)


    def test_get_2015(self):
        response = self.anon_user.get('/2015')
        data = self.assert200(response)
        self.assertTrue('Test 2015 article' in data)
        self.assertFalse('Test 2016 article' in data)


class WritePostTest(UserTestCase, HTTPTestMixin):

    def test_get_write_form(self):
        self.assert200(self.admin_user.get('/blog'))


    def test_write_post(self):
        contents = {
            'title': 'Test article',
            'slug': 'test-article',
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
