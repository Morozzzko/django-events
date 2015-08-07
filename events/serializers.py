# -*- coding: utf-8 -*-

from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Profile, Team


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('additional_name', 'birth_date', 'telephone', )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff', 'first_name', 'last_name', 'url', )

    def to_representation(self, instance):
        representation_user = serializers.ModelSerializer.to_representation(self, instance)
        profile = instance.profile
        representation_profile = ProfileSerializer(context=self.context).to_representation(profile)
        for key in ProfileSerializer.Meta.fields:
            representation_user[key] = representation_profile[key]
        return representation_user

    def to_internal_value(self, data):
        return serializers.ModelSerializer.to_internal_value(self, data)


class TeamSerializer(serializers.ModelSerializer):
    curator = serializers.HyperlinkedRelatedField(view_name='user-detail',
                                                  queryset=User.objects.all(),
                                                  allow_null=True)
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'curator', 'members', 'url', )

    def to_representation(self, instance):
        result = serializers.ModelSerializer.to_representation(self, instance)
        if instance.curator:
            result['curator'] = UserSerializer(context=self.context).to_representation(instance.curator)
        return result


