from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Event, DrinkEvent


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'events', 'drink_events', 'password')
		read_only_fields = ('events', 'drink_events')
		extra_kwargs = {
			'password': {'write_only': True}
		}

	def create(self, validated_data):
		user = User(username=validated_data['username'])
		user.set_password(validated_data['password'])
		user.save()
		return user


class UserIdAndUsernameSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username')


class DrinkEventSerializer(serializers.ModelSerializer):
	class Meta:
		model = DrinkEvent
		fields = ('id', 'user', 'event', 'datetime')


class EventSerializer(serializers.ModelSerializer):
	drink_events = DrinkEventSerializer(many=True, read_only=True)
	users = UserIdAndUsernameSerializer(many=True, read_only=True)

	class Meta:
		model = Event
		fields = ('id', 'start_datetime', 'end_datetime', 'name', 'owner', 'users', 'drink_events')
		read_only_fields = ('end_datetime', 'owner', 'users')


class CreateEventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ('name',)
