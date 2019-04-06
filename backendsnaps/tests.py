from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory


User = get_user_model()


class LoginTestCase(TestCase):
	def test_login(self):
		user = User.objects.create(username='test')
		user.set_password('test')
		user.save()

		c = Client()
		r = c.post('/api-token-auth/', {'username': 'test', 'password': 'test'})

		self.assetEqual(r.status_code, 200)
