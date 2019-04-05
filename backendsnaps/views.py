from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event, DrinkEvent
from .serializers import UserSerializer, EventSerializer, DrinkEventSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects
	serializer_class = UserSerializer


class EventViewSet(viewsets.ModelViewSet):
	queryset = Event.objects
	serializer_class = EventSerializer

	@action(detail=False, methods=['post'])
	def join_event(self, request):
		self.get_object().users.add(self.user)
		return Response({'success': True})


class DrinkEventViewSet(viewsets.ModelViewSet):
	queryset = DrinkEvent.objects
	serializer_class = DrinkEventSerializer

	def get_queryset(self):
		qs = DrinkEvent.objects

		filters = ['user', 'event']

		for k in filters:
			if k in self.request.GET:
				qs = qs.filter(**{k: self.request.GET[k]})

		return qs
