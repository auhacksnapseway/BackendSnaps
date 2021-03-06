import json
import datetime

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APIRequestFactory, force_authenticate

from .models import Event, DrinkEvent
from .serializers import UserSerializer, EventSerializer, DrinkEventSerializer, CreateEventSerializer

User = get_user_model()


class CreateOrAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True

        return super().has_permission(request, view)


class OwnsEvent(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class InEvent(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.users.filter(pk=request.user.id).exists()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (CreateOrAuthenticated,)
    queryset = User.objects
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        return Response(UserSerializer(request.user).data)


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects
    serializer_class = EventSerializer

    def create(self, request):
        s = CreateEventSerializer(data=request.data)
        if not s.is_valid():
            return Response({'detail': 'name parameter is probably bad'}, status=status.HTTP_400_BAD_REQUEST)

        event = Event.objects.create(owner=request.user, name=s.validated_data['name'])
        event.users.add(request.user)

        return Response({'id': event.id})


    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        event = self.get_object()
        if event.users.filter(pk=request.user.id).exists():
            return Response({'detail': 'User has already joined the event'}, status=status.HTTP_400_BAD_REQUEST)

        if event.is_stopped:
            return Response({'detail': 'Event has ended'}, status=status.HTTP_400_BAD_REQUEST)

        event.users.add(request.user)
        return Response({})

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        event = self.get_object()
        if not event.users.filter(pk=request.user.id).exists():
            return Response({'detail': 'User is not in the event'}, status=status.HTTP_400_BAD_REQUEST)

        event.users.remove(request.user)
        return Response({})

    @action(detail=True, methods=['post'], permission_classes=(OwnsEvent,))
    def stop(self, request, pk=None):
        event = self.get_object()
        if event.is_stopped:
            return Response({'detail': 'Event has already been stopped'}, status=status.HTTP_400_BAD_REQUEST)

        event.stop()
        return Response({})

    @action(detail=True, methods=['post'], permission_classes=(InEvent,))
    def create_drinkevent(self, request, pk=None):
        MINIMUM_DURATION = datetime.timedelta(seconds=10)

        event = self.get_object()
        if event.is_stopped:
            return Response({'detail': 'Event has ended'}, status=status.HTTP_400_BAD_REQUEST)

        drink_events = request.user.get_drink_events(event).order_by('datetime')
        if drink_events.exists():
            last_dt = drink_events.last().datetime
            if timezone.now() - last_dt < MINIMUM_DURATION:
                return Response({'detail': 'Too soon, try again later'}, status=status.HTTP_400_BAD_REQUEST)

        drinkevent = DrinkEvent.objects.create(user=request.user, event=self.get_object())
        return Response({'id': drinkevent.id})


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


    def create(self, request):
        return Response({'detail': 'Not allowed'}, status=status.HTTP_400_BAD_REQUEST)


def get_user_data():
    factory = APIRequestFactory()
    user = User.objects.get(username='test')
    view = UserViewSet.as_view({'get': 'list'})

    request = factory.get('/users/')
    force_authenticate(request, user=user)
    response = view(request)
    return response.data


def get_event_data():
    factory = APIRequestFactory()
    user = User.objects.get(username='test')
    view = EventViewSet.as_view({'get': 'retrieve'})

    request = factory.get('/events/')
    force_authenticate(request, user=user)
    response = view(request, pk=1)
    return response.data


def index(request):
    context = {
        'user_data': json.dumps(get_user_data()),
        'event_data': json.dumps(get_event_data()),
    }

    return render(request, 'chart.html', context)
