from django.contrib.auth import get_user_model

from rest_framework import viewsets

from .models import Event, DrinkEvent
from .serializers import UserSerializer, EventSerializer, DrinkEventSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects
	serializer_class = UserSerializer


class EventViewSet(viewsets.ModelViewSet):
	queryset = Event.objects
	serializer_class = EventSerializer


class DrinkEventViewSet(viewsets.ModelViewSet):
	queryset = DrinkEvent.objects
	serializer_class = DrinkEventSerializer
