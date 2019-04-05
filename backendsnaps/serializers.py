from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Event, DrinkEvent


class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = get_user_model()
		fields = ('username',)


class EventSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Event
		fields = ('start_datetime', 'end_datetime', 'name', 'owner', 'users')


class DrinkEventSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = DrinkEvent
		fields = ('user', 'event', 'datetime')
