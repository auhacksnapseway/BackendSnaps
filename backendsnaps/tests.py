from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils import timezone
import random

from .models import Event

User = get_user_model()


def create_test_user():
    user = User.objects.create(username='test')
    user.set_password('test')
    user.save()

    user_2 = User.objects.create(username="testboi")
    user_2.set_password("OK")
    user_2.save()


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
        r_login_success = c.post('/api-token-auth/', {'username': 'utest2', 'password': 'utest2'})
        self.assertEqual(r_login_success.status_code, 200)


class LoginTestCase(TestCase):
    def test_login_failure(self):
        c = Client()
        r = c.post('/api-token-auth/', {'username': 'testzzz', 'password': 'test'})
        self.assertEqual(r.status_code, 400)
        self.assertTrue(r.json()['non_field_errors'], 'Unable to log in with provided credentials.')


class EventTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    def test_events_join(self):
        token = get_test_token_user(self)
        event = Event.objects.create(name='foo', owner=User.objects.get(username='test'))

        r = self.c.post(f'/api/events/{event.id}/join/', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(r.status_code, 200)

        # fail when joining again
        r = self.c.post(f'/api/events/{event.id}/join/', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(r.json()['detail'], 'User has already joined the event')

    def test_events_create(self):
        token = get_test_token_user(self)
        r = self.c.post('/api/events/', {'name': 'foo'}, HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(200, r.status_code)
        created_event = Event.objects.get(name="foo")
        self.assertIsNotNone(created_event)


class DrinkEventTestCase(TestCase):
    def test_drink_events(self):
        token = get_test_token_user(self)
        t_user = User.objects.get(username='test');
        t_boi = User.objects.get(username="testboi")
        event = Event.objects.create(name='foo', owner=t_user)
        event.users.add(t_user)
        event.users.add(t_boi)

        c = Client()
        r_login = c.post('/api-token-auth/', {'username': 'testboi', 'password': 'OK'}).json()['token']
        r = c.post(f'/api/events/{event.id}/create_drinkevent/', HTTP_AUTHORIZATION=f'Token {token}')

        c.post(f'/api/events/{event.id}/create_drinkevent/', HTTP_AUTHORIZATION=f'Token {r_login}')
        c.post(f'/api/events/{event.id}/create_drinkevent/', HTTP_AUTHORIZATION=f'Token {r_login}')
        self.assertEqual(r.status_code, 200)
