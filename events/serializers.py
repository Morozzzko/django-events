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
    status = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()

    middle_name = serializers.CharField(source='profile.middle_name',
                                        allow_blank=True,
                                        allow_null=True)
    telephone = serializers.CharField(source='profile.telephone',
                                      allow_blank=True,
                                      allow_null=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'middle_name',
                  'email', 'telephone',
                  'is_staff', 'is_superuser', 'status', 'team', 'url',)
        fields_short = ('username', 'first_name', 'last_name', 'status', 'url',)
        read_only_fields = ('is_superuser',)
        write_only_fields = ('password',)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)

        for attr in validated_data.keys():
            data = validated_data.get(attr, getattr(instance, attr))
            setattr(instance, attr, data)

        instance.save()

        if profile_data:
            for attr in profile_data:
                setattr(instance.profile, attr, profile_data.get(attr))

            instance.profile.save()

        return instance

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)

        password = validated_data.pop('password', None)

        instance = self.Meta.model(**validated_data)

        if password:
            instance.set_password(password)

        instance.save()

        if profile_data:
            for attr in profile_data:
                setattr(instance.profile, attr, profile_data.get(attr))
            instance.profile.save()

        return instance

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
