# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .models import Team, PresenceStatus, TeamMembership
from .serializers import UserSerializer, TeamSerializer, StatusSerializer, TeamMembershipSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

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
        return Response(serializer.errors)


class StatusViewSet(viewsets.GenericViewSet):
    queryset = PresenceStatus.objects.all()
    serializer_class = StatusSerializer

    def retrieve(self, request, pk=None):
        status = get_object_or_404(self.queryset, user=pk)
        serializer = StatusSerializer(status, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        status = get_object_or_404(self.queryset, user=pk)
        if type(request.data) == int:
            serializer = StatusSerializer(status, data={'status': request.data}, context={'request': request})
        else:
            serializer = StatusSerializer(status, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
