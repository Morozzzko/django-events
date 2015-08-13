# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model

from rest_framework import serializers

from collections import OrderedDict

from .models import Profile, Team, TeamMembership, PresenceStatus


class StatusSerializer(serializers.HyperlinkedModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = PresenceStatus
        fields = ('user', 'status', 'last_modified', 'url', 'text', )

    def get_text(self, instance):
        return PresenceStatus.Options.label(instance.status)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'is_staff', 'first_name', 'last_name', 'url', 'status', )
        depth = 2

    def get_status(self, instance):
        status = PresenceStatus.objects.get(user=instance)
        return StatusSerializer(status, context={'request': self.context['request']}).data


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['additional_name', 'birth_date', 'telephone', ]

    def to_representation(self, instance):
        representation_profile = super(ProfileSerializer, self).to_representation(instance)
        user = instance.user
        representation_user = UserSerializer(user, context={'request': self.context['request']}).to_representation(user)
        for key in representation_user:
            representation_profile[key] = representation_user[key]
        return representation_profile

    def to_internal_value(self, data):
        data_user = OrderedDict()
        for key in ProfileSerializer.Meta.fields:
            if key in data:
                data_user[key] = data[key]
                data.pop(key)

        user_tmp = self.user
        self.user = UserSerializer()
        user_internal = UserSerializer(context={'request': self.context['request']}, partial=True)\
            .to_internal_value(data_user)
        self.user = user_tmp
        return super(ProfileSerializer, self).to_internal_value(data)


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'curator', 'members', 'url', )

    def get_members(self, instance):
        memberships = TeamMembership.objects.filter(team=instance)
        members = (x.user for x in memberships)
        profiles = Profile.objects.filter(user__in=members)
        profiles_serialized = [ProfileSerializer(x, context={'request': self.context['request']}).data for x in profiles]
        return profiles_serialized

    def to_representation(self, instance):
        result = serializers.ModelSerializer.to_representation(self, instance)
        if instance.curator:
            result['curator'] = UserSerializer(context={'request': self.context['request']})\
                .to_representation(instance.curator)
        return result

