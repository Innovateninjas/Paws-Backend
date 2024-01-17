from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

#test for login
class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)

    def test_login_success(self):
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['token'], self.token.key)

    def test_login_failure(self):
        response = self.client.post('/login/', {'username': 'wronguser', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Wrong Credentials')