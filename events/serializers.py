# -*- coding: utf-8 -*-

from django.contrib.auth.models import User

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


class MinimalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'url', )


class TeamSerializer(serializers.ModelSerializer):
    curator = serializers.HyperlinkedRelatedField(view_name='user-detail',
                                                  queryset=User.objects.all(),
                                                  allow_null=True)
    members = MinimalUserSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'curator', 'members', 'url')

    def to_representation(self, instance):
        result = serializers.ModelSerializer.to_representation(self, instance)
        if instance.curator:
            result['curator'] = MinimalUserSerializer(context=self.context).to_representation(instance.curator)
        return result


