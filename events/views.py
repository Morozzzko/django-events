# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from .models import Team, PresenceStatus
from .serializers import UserSerializer, TeamSerializer, StatusSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        user_type = self.kwargs.get('type', None)
        if user_type == 'attendees':
            return get_user_model().objects.filter(is_staff=False, is_superuser=False)
        elif user_type == 'organizers':
            return get_user_model().objects.filter(Q(is_staff=True) | Q(is_superuser=True))
        return get_user_model().objects.all()

    @detail_route(['GET'])
    def status(self, request, pk):
        presence_status = PresenceStatus.objects.get(user=pk)
        serializer = StatusSerializer(presence_status, context={'request': request})
        return Response(serializer.data)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
