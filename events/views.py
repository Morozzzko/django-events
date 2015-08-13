# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth import get_user_model

from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .models import Team, PresenceStatus
from .serializers import UserSerializer, TeamSerializer, StatusSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    @detail_route(['GET'])
    def status(self, request, pk):
        presence_status = get_object_or_404(PresenceStatus, user=pk)
        serializer = StatusSerializer(presence_status, context={'request': request})
        return Response(serializer.data)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
