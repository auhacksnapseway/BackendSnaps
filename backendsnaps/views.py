from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Event, DrinkEvent
from .serializers import UserSerializer, EventSerializer, DrinkEventSerializer, CreateEventSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects
	serializer_class = UserSerializer


class EventViewSet(viewsets.ModelViewSet):
	permission_classes = (IsAuthenticated,)
	queryset = Event.objects
	serializer_class = EventSerializer

	@action(detail=False, methods=['post'])
	def create_event(self, request):
		s = CreateEventSerializer(data=request.data)
		if not s.is_valid():
			return Response({'success': False})

		event = Event.objects.create(owner=request.user, name=s.validated_data['name'])
		event.users.add(request.user)

		return Response({'success': True})

	@action(detail=True, methods=['post'])
	def join_event(self, request, pk=None):
		self.get_object().users.add(request.user)
		return Response({'success': True})

	@action(detail=True, methods=['post'])
	def leave_event(self, request, pk=None):
		self.get_object().users.remove(request.user)
		return Response({'success': True})

	@action(detail=True, methods=['post'])
	def stop_event(self, request, pk=None):
		self.get_object().stop()
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
