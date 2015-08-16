# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.settings import api_settings
from rest_framework.reverse import reverse

from collections import OrderedDict

from .models import Profile, Team, TeamMembership, PresenceStatus


class DynamicFieldsHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.

    Copied from
    http://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
    and edited to work with HyperlinkedModelSerializer
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsHyperlinkedModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class FullAndShortModelSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        self.short = kwargs.pop('short', False)

        assert hasattr(self.Meta, 'fields_short'), "FullAndShort model must specify fiels_short"

        super(FullAndShortModelSerializer, self).__init__(*args, **kwargs)

        if self.short:
            fields = set(self.fields.keys())
            fields_short = set(self.Meta.fields_short)
            for field_name in fields - fields_short:
                self.fields.pop(field_name)


class StatusSerializer(FullAndShortModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = PresenceStatus
        fields = ('user', 'status', 'last_modified', 'text', 'url',)
        fields_short = ('status', 'text', 'url',)
        extra_kwargs = {
            'url': {'view_name': 'user-status'}
        }

    def get_text(self, instance):
        return PresenceStatus.Options.label(instance.status)

    def to_representation(self, instance):
        representation = super(StatusSerializer, self).to_representation(instance)
        if api_settings.URL_FIELD_NAME in representation:
            request = self.context.get('request')
            url = request.build_absolute_uri(reverse('user-status', args=[instance.user.pk]))
            representation[api_settings.URL_FIELD_NAME] = url
        return representation


class UserSerializer(FullAndShortModelSerializer):
    username = serializers.CharField(read_only=True)
    status = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_staff', 'is_superuser', 'status', 'team', 'url',)
        fields_short = ('username', 'first_name', 'last_name', 'status', 'url',)
        depth = 2

    def get_status(self, instance):
        status, __ = PresenceStatus.objects.get_or_create(user=instance)
        return StatusSerializer(status,
                                context={'request': self.context['request']},
                                short=self.short).data

    def get_team(self, instance):
        team_membership, __ = TeamMembership.objects.get_or_create(user=instance, defaults={'team': None})
        if team_membership.team is None:
            return None
        return TeamSerializer(team_membership.team,
                              context={'request': self.context['request']},
                              short=True).data


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
        user_internal = UserSerializer(context={'request': self.context['request']}, partial=True) \
            .to_internal_value(data_user)
        self.user = user_tmp
        return super(ProfileSerializer, self).to_internal_value(data)


class TeamSerializer(FullAndShortModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'curator', 'members', 'url',)
        fields_short = ('name', 'url',)

    def get_members(self, instance):
        memberships = TeamMembership.objects.filter(team=instance)
        members = [x.user for x in memberships]
        profiles_serialized = [UserSerializer(x,
                                              context={'request': self.context['request']},
                                              short=True).data for x in members]
        return profiles_serialized

    def to_representation(self, instance):
        result = serializers.ModelSerializer.to_representation(self, instance)
        if instance.curator and not self.short:
            result['curator'] = UserSerializer(instance.curator,
                                               context={'request': self.context['request']},
                                               short=True).data
        return result
