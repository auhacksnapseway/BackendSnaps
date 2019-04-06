import random

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class User(AbstractUser):
    objects = CustomUserManager()

    def get_drink_events(self, event):
        return DrinkEvent.objects.filter(user=self, event=event)

    def get_score(self, event):
        return self.get_drink_events(event).count()


class Event(models.Model):
    start_datetime = models.DateTimeField(auto_now_add=True)
    end_datetime = models.DateTimeField(blank=True, null=True)

    name = models.TextField()

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_events')
    users = models.ManyToManyField(User, related_name='events')

    def __str__(self):
        return f'{self.name} ({self.start_datetime.date()})'

    def stop(self):
        self.end_datetime = timezone.now()
        self.save()

    @property
    def is_stopped(self):
        return self.end_datetime is not None

	def update_owner(self):
		latest_drink_event = self.owner.drink_events.order_by('datetime').last()
		one_hour_extra = timezone.now() + timezone.timedelta(hours=1)
		diff_minutes = (one_hour_extra - latest_drink_event.datetime).seconds // 60
		chad_check = random.uniform(59.5, 120.5)
		if diff_minutes < chad_check:
			event_participants = self.users.all()
			best_score = 0; best_performer = None
			for participant in event_participants:
				cur_score = participant.get_score(self)
				if best_score < cur_score and participant != self.owner:
					best_score = cur_score
					best_performer = participant
			if best_performer is not None:
				self.owner = None
				self.owner = best_performer


#todo: 1)owner is not None 2) move prev owner into participants 3) check users is not None, #do nothing if owner is highest

class DrinkEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='drink_events')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='drink_events')

    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} ({self.datetime})'

	def save(self, **kwargs):
		super().save(**kwargs)
		self.event.update_owner()
