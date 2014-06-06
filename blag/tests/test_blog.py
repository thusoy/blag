# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from . import UserTestCase, HTTPTestMixin
from .. import db
from ..models import BlogPost, slugify

import json
import unittest


class BlogTest(UserTestCase, HTTPTestMixin):

    def setUp(self):
        with self.app.app_context():
            db.session.add(BlogPost(title='Test article', rendered_content='Snip', raw_content='Snip'))
            db.session.commit()
            self.post_id = BlogPost.query.first().id


    def test_main_page(self):
        response = self.anon_user.get('/')
        data = self.assert200(response)
        self.assertTrue('Test article' in data.decode('utf-8'))
        self.assertTrue('Snip' in data.decode('utf-8'))


    def test_post_details(self):
        response = self.anon_user.get('/blag/%d' % self.post_id)
        data = self.assert200(response)
        self.assertTrue('Test article' in data.decode('utf-8'))
        self.assertTrue('Snip' in data.decode('utf-8'))


    def test_styleguide(self):
        response = self.anon_user.get('/styleguide')
        self.assert200(response)


class WritePostTest(UserTestCase, HTTPTestMixin):

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


class UtilTest(unittest.TestCase):

    def test_slugify(self):
        tests = (
            ("Picture of John Lennon rockin'", 'picture-of-john-lennon-rockin'),
            ("J'ai parlée français, un peu", 'jai-parlee-francais-un-peu'),
            ("I'm Tarjei Husøy, gentleman of leisure", 'im-tarjei-husoy-gentleman-of-leisure'),
        )
        for value, expected in tests:
            self.assertEqual(slugify(value), expected)
