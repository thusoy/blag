from . import UserTestCase, HTTPTestMixin

class LoginTest(UserTestCase, HTTPTestMixin):

    def test_get_login(self):
        response = self.anon_user.get('login')
        data = self.assert200(response)


    def test_login_valid(self):
        response = self.anon_user.post('/login', data={
            'password': 'password',
            'email': 'bob@example.com'
        })
        self.assert302(response)


    def test_login_invalid(self):
        response = self.anon_user.post('/login', data={
            'password': 'notthepassword',
            'email': 'bob@example.com',
        })
        self.assert401(response)


    def test_login_unknown_user(self):
        response = self.anon_user.post('/login', data={
            'password': 'notthepassword',
            'email': 'anna@example.com',
        })
        self.assert401(response)


    def test_logout(self):
        response = self.admin_user.get('/logout')
        self.assert302(response)
