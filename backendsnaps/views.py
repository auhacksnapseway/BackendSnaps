from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Event, DrinkEvent
from .serializers import UserSerializer, EventSerializer, DrinkEventSerializer, CreateEventSerializer


User = get_user_model()


class CreateOrAuthenticated(IsAuthenticated):
	def has_permission(self, request, view):
		if request.method == 'POST':
			return True

		return super().has_permission(request, view)


class UserViewSet(viewsets.ModelViewSet):
	permission_classes = (CreateOrAuthenticated,)
	queryset = User.objects
	serializer_class = UserSerializer


class EventViewSet(viewsets.ModelViewSet):
	permission_classes = (IsAuthenticated,)
	queryset = Event.objects
	serializer_class = EventSerializer

	def create(self, request):
		s = CreateEventSerializer(data=request.data)
		if not s.is_valid():
			return Response({'success': False})

		event = Event.objects.create(owner=request.user, name=s.validated_data['name'])
		event.users.add(request.user)

		return Response({'success': True})

	@action(detail=True, methods=['post'])
	def join(self, request, pk=None):
		self.get_object().users.add(request.user)
		return Response({'success': True})

	@action(detail=True, methods=['post'])
	def leave(self, request, pk=None):
		self.get_object().users.remove(request.user)
		return Response({'success': True})

	@action(detail=True, methods=['post'])
	def stop(self, request, pk=None):
		self.get_object().stop()
		return Response({'success': True})

	@action(detail=True, methods=['post'])
	def create_drinkevent(self, request, pk=None):
		DrinkEvent.objects.create(user=request.user, event=self.get_object())
		return Response({'success': True})


class DrinkEventViewSet(viewsets.ModelViewSet):
	permission_classes = (IsAuthenticated,)
	queryset = DrinkEvent.objects
	serializer_class = DrinkEventSerializer

	def get_queryset(self):
		qs = DrinkEvent.objects

		filters = ['user', 'event']

		for k in filters:
			if k in self.request.GET:
				qs = qs.filter(**{k: self.request.GET[k]})

		return qs
