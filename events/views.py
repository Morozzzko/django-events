# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User

from rest_framework import generics, viewsets, permissions

from .models import Profile, Team
from .serializers import UserSerializer, TeamSerializer, ProfileSerializer


class UserList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

