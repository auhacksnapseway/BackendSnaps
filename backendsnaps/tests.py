from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory


User = get_user_model()


def create_test_user():
	user = User.objects.create(username='test')
	user.set_password('test')
	user.save()


def get_test_token():
	create_test_user()

	c = Client()
	r = c.post('/api-token-auth/', {'username': 'test', 'password': 'test'})

	self.assetEqual(r.status_code, 200)

	return r.json['token']


class LoginTestCase(TestCase):
	def test_login(self):
		get_test_token()


class EventTestCase(TestCase):
	def test_join(self):
		token = get_test_token()
		event = Event.objects.create(name='foo')

		c = Client()

		c.post(HTTP_Authorization=f'Token {token}'))
