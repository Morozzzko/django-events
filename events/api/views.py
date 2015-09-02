# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy

from events.models import Team, PresenceStatus, TeamMembership, Event
from events.api.serializers import UserSerializer, TeamSerializer, StatusSerializer, TeamMembershipSerializer, \
    EventSerializer


class APIEntry(APIView):
    def get(self, request):
        links = {
            'teams': reverse_lazy('team-list', request=request),
            'users': {
                'all': reverse_lazy('user-list', request=request),
                'organizers': reverse_lazy('user-list-organizers', request=request),
                'attendees': reverse_lazy('user-list-attendees', request=request),
            },
            'event': reverse_lazy('event-detail', request=request),
        }
        return Response(links)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('last_name', 'first_name')
    ordering = ('last_name', 'first_name')

    def get_queryset(self):
        user_type = self.kwargs.get('type', None)
        if user_type == 'attendees':
            return get_user_model().objects.filter(is_staff=False, is_superuser=False)
        elif user_type == 'organizers':
            return get_user_model().objects.filter(Q(is_staff=True) | Q(is_superuser=True))
        return get_user_model().objects.all()

    @detail_route(methods=['get', 'put'])
    def status(self, request, pk):
        presence_status, __ = PresenceStatus.objects.get_or_create(user=pk)
        serializer = StatusSerializer(presence_status, context={'request': request})
        return Response(serializer.data)


class TeamMembershipViewSet(viewsets.GenericViewSet):
    queryset = TeamMembership.objects.all()
    serializer_class = TeamMembershipSerializer

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(self.queryset, user=pk)
        serializer = TeamMembershipSerializer(instance, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = get_object_or_404(self.queryset, user=pk)
        serializer = TeamMembershipSerializer(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatusViewSet(viewsets.GenericViewSet):
    queryset = PresenceStatus.objects.all()
    serializer_class = StatusSerializer

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(self.queryset, user=pk)
        serializer = StatusSerializer(instance, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = get_object_or_404(self.queryset, user=pk)
        if type(request.data) == int:
            serializer = StatusSerializer(instance, data={'status': request.data}, context={'request': request})
        else:
            serializer = StatusSerializer(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name',)
    ordering = ('name',)


class EventViewSet(viewsets.GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def retrieve(self, request):
        instance = Event.get_solo()
        serializer = EventSerializer(instance, context={'request': request})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request):
        instance = Event.get_solo()
        serializer = EventSerializer(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request):
        instance = Event.get_solo()
        serializer = EventSerializer(instance, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
