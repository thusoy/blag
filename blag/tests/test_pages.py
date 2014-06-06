from . import UserTestCase

class PagesTest(UserTestCase):

    def test_me_page(self):
        response = self.anon_user.get('/me')
        self.assert200(response)
