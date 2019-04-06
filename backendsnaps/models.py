from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
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



class DrinkEvent(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='drink_events')
	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='drink_events')

	datetime = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user} ({self.datetime})'

