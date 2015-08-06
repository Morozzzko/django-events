# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from rest_framework import generics

from .models import Profile, Team
from .serializers import UserSerializer, TeamSerializer


class UserList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


def blank(request):
    pass
