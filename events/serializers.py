# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Profile, Team


class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='user.pk')
    username = serializers.CharField(source='user.username')
    given_name = serializers.CharField(source='user.first_name')
    family_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    is_staff = serializers.BooleanField(source='user.is_staff')

    class Meta:
        model = Profile
        fields = ('id', 'username', 'given_name', 'additional_name', 'family_name', 'email', 'telephone', 'status',
                  'is_staff', 'url', )
        extra_kwargs = {
            'url': {'view_name': 'user-detail', 'lookup_field': 'pk'},
            'users': {'lookup_field': 'username'}
        }


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='user.pk')
    name = serializers.CharField(source='group.name')

    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'owner', 'url',)
        extra_kwargs = {
            'url': {'view_name': 'group-detail', 'lookup_field': 'pk'},
            'users': {'lookup_field': 'username'}
        }