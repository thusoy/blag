from .. import create_app

import unittest

class BlogTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()


    def test_main_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
