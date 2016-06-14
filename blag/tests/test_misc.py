from . import UserTestCase, HTTPTestMixin

class BlogTest(UserTestCase, HTTPTestMixin):

    def test_main_page(self):
        response = self.anon_user.get('/robots.txt')
        data = self.assert200(response)
