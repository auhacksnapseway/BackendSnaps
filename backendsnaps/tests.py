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


class UserTestCase(TestCase):
    def test_create_user(self):
        c = Client()
        r = c.post('/api/users/', {'username': 'utest2', 'password': 'utest2'})
        self.assertEqual(r.status_code, 201)
        r_login_success = c.post('/api-token-auth/', {'username':'utest2', 'password':'utest2'})
        self.assertEqual(r_login_success.status_code, 200)


class LoginTestCase(TestCase):
    def test_login_failure(self):
        c = Client()
        r = c.post('/api-token-auth/', {'username': 'testzzz', 'password': 'test'})
        self.assertEqual(r.status_code, 400)
        self.assertTrue(r.json()['non_field_errors'], 'Unable to log in with provided credentials.')

#test: if join first time, success: second time: fail
class EventTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    def test_events_join(self):
        token = get_test_token_user(self)
        event = Event.objects.create(name='foo', owner=User.objects.get(username='test'))

        r = self.c.post(f'/api/events/{event.id}/join/', HTTP_AUTHORIZATION=f'Token {token}')

        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()['success'])

        #fail when joining again
        r = self.c.post(f'/api/events/{event.id}/join/', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(r.json()['success'], False)

    def test_events_create(self):
        token = get_test_token_user(self)
        owner = User.objects.get(username='test')

        r = self.c.post('/api/events/', {'name': 'foo'}, HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(200, r.status_code)
        created_event = Event.objects.get(name="foo")
        self.assertIsNotNone(created_event)



class DrinkEventTestCase(TestCase):
    def test_drink_events(self):
        token = get_test_token_user(self)
        event = Event.objects.create(name='foo', owner=User.objects.get(username='test'))

        c = Client()
        r = c.post(f'/api/events/{event.id}/create_drinkevent/', HTTP_AUTHORIZATION=f'Token {token}')

        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()['success'])
