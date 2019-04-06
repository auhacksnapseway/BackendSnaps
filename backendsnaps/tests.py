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
        r_login_success = c.post('/api-token-auth/', {'username':'utest2', 'password':'utest2'})
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
        self.assertTrue(r.json()['success'])

        #fail when joining again
        r = self.c.post(f'/api/events/{event.id}/join/', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(r.json()['success'], False)

    def test_events_create(self):
        token = get_test_token_user(self)
        r = self.c.post('/api/events/', {'name': 'foo'}, HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(200, r.status_code)
        created_event = Event.objects.get(name="foo")
        self.assertIsNotNone(created_event)

    def get_owner_event(self):
        #setup
        token = get_test_token_user(self)
        user_2 = User.objects.get(username='testboi')
        #create event with user
        event = Event.objects.create(name='foo', owner=User.objects.get(username='test'))
        event.users.add(user_2)
        #create drinkevent
        self.c.post(f'/api/events/{event.id}/create_drinkevent/', HTTP_AUTHORIZATION=f'Token {token}')
        r = self.c.get(f'/api/events/{event.id}/', HTTP_AUTHORIZATION=f'Token {token}')
        #add user to drink_event
        r_u2_response = self.c.post('/api-token-auth/', {'username': 'testboi', 'password': 'OK'})
        self.c.post(f'/api/events/{event.id}/create_drinkevent/', HTTP_AUTHORIZATION=f'Token {r_u2_response.json()["token"]}')

        #find latest drink event
        owner = User.objects.get(pk=r.data['owner'])
        latest_drink_event = owner.drink_events.order_by('datetime').last()
        one_hour_extra = timezone.now() + timezone.timedelta(hours=1)
        #see if drink was to late
        #find minutes
        diff_minutes = (one_hour_extra - latest_drink_event.datetime).seconds//60
        chad_check = random.uniform(59.5, 120.5)
        is_weak_drinker = diff_minutes < chad_check

        if is_weak_drinker:
            event_participants = event.users.all()
            cur = 0; best_performer = None
            for participant in event_participants:
                print(participant.get_score(event))
                #cur = max(cur, participant.get_score(event))
                cur_score = participant.get_score(event)
                if cur < cur_score:
                    cur = cur_score
                    best_performer = participant
            #print(cur)
            #find 2nd highest drinker (DONE)
            #set 2nd highest drinker to owner
            event.owner = best_performer
            print(event.owner)
        return None
            #change ownership
    #def _get_second_drinker(self, ):



class DrinkEventTestCase(TestCase):
    def test_drink_events(self):
        token = get_test_token_user(self)
        event = Event.objects.create(name='foo', owner=User.objects.get(username='test'))

        c = Client()
        r = c.post(f'/api/events/{event.id}/create_drinkevent/', HTTP_AUTHORIZATION=f'Token {token}')

        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()['success'])
