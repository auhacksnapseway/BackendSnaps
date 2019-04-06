from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Event


User = get_user_model()


def create_test_user():
	user = User.objects.create(username='test')
	user.set_password('test')
	user.save()



def get_test_token_user(t):
	create_test_user()

	c = Client()
	r = c.post('/api-token-auth/', {'username': 'test', 'password': 'test'})

	t.assertEqual(r.status_code, 200)

	return r.json()['token']



class LoginTestCase(TestCase):
	def setUp(self):
		token = get_test_token_user(self)

	def test_login(self):
		return None


class EventTestCase(TestCase):
	def test_events(self):
		token = get_test_token_user(self)
		event = Event.objects.create(name='foo', owner=User.objects.get(username='test'))

		c = Client()
		r = c.post(f'/api/events/{event.id}/join/', HTTP_AUTHORIZATION=f'Token {token}')

		self.assertEqual(r.status_code, 200)
		self.assertTrue(r.json()['success'])


class DrinkEventTestCase(TestCase):
	def test_drink_events(self):
		token = get_test_token_user(self)
		event = Event.objects.create(name='foo', owner=User.objects.get(username='test'))

		c = Client()
		r = c.post(f'/api/events/{event.id}/create_drinkevent/', HTTP_AUTHORIZATION=f'Token {token}')

		self.assertEqual(r.status_code, 200)
		self.assertTrue(r.json()['success'])


