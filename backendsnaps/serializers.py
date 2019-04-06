from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Event, DrinkEvent


User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
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


class EventSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Event
		fields = ('id', 'start_datetime', 'end_datetime', 'name', 'owner', 'users')
		read_only_fields = ('end_datetime', 'owner', 'users')


class DrinkEventSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = DrinkEvent
		fields = ('id', 'user', 'event', 'datetime')


class CreateUserSerializer(serializers.Serializer):
	class Meta:
		model = User
		fields = ('username', 'password')
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		user = User(username=validated_data['username'])
		user.set_password(validated_data['password'])
		user.save()
		return user


class CreateEventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ('name',)
