from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory


User = get_user_model()


class LoginTestCase(TestCase):
	def test_login(self):
		user = User.objects.create(username='test')
		user.set_password('test')
		user.save()

		factory = APIRequestFactory()
		r = factory.post('/api-auth/login/', {'username': 'test', 'password': 'test'})
		print(r)
		print(str(r.content, 'utf-8'))

		'''
		c = Client()
		r = c.post('/api-auth/login/', {'username': 'test', 'password': 'test'})
		print(str(r.content, 'utf-8'))
		'''


# Create your tests here.
