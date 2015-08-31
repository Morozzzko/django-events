# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.settings import api_settings
from rest_framework.reverse import reverse

from events.models import Team, TeamMembership, PresenceStatus


class DynamicFieldsHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    """
    A HyperlinkedModelSerializer that takes an additional `fields` argument that
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


class TeamMembershipSerializer(DynamicFieldsHyperlinkedModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = TeamMembership
        fields = ('team_name', 'team', 'username', 'user', 'role', 'url',)
        read_only_fields = ('user', 'username', 'team_name',)
        extra_kwargs = {
            'url': {'view_name': 'user-team'}
        }

    def to_representation(self, instance):
        representation = super(TeamMembershipSerializer, self).to_representation(instance)
        if 'team_name' in representation and representation['team_name'] is None:
            representation['team_name'] = ""
        return representation


class StatusSerializer(DynamicFieldsHyperlinkedModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = PresenceStatus
        fields = ('user', 'status', 'last_modified', 'text', 'url',)
        read_only_fields = ('user', 'last_modified', 'text',)
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


class UserSerializer(DynamicFieldsHyperlinkedModelSerializer):
    status = StatusSerializer(source='presencestatus',
                              fields=('status', 'text', 'last_modified', 'url',))
    team_membership = TeamMembershipSerializer(source='teammembership',
                                               fields=('team', 'team_name', 'role', 'url',))

    middle_name = serializers.CharField(source='profile.middle_name',
                                        allow_blank=True,
                                        allow_null=True)
    telephone = serializers.CharField(source='profile.telephone',
                                      allow_blank=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'middle_name',
                  'email', 'telephone', 'team_membership',
                  'is_staff', 'is_superuser', 'status', 'url',)
        read_only_fields = ('is_superuser',)
        write_only_fields = ('password',)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)

        password = validated_data.pop('password', None)

        if password:
            instance.set_password(password)

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


class TeamSerializer(DynamicFieldsHyperlinkedModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'curator', 'members', 'url',)
        fields_curator = ('id', 'username', 'first_name', 'last_name', 'status', 'url',)
        fields_members = ('id', 'username', 'first_name', 'last_name', 'status', 'team_membership', 'url',)
        fields_membership = ('role', 'url',)

    def get_members(self, instance):
        memberships = TeamMembership.objects.filter(team=instance)
        members = [x.user for x in memberships]
        profiles_serialized = list()
        for user in members:
            user_data = UserSerializer(
                user,
                context={'request': self.context['request']},
                fields=self.Meta.fields_members).data
            for key in set(user_data['team_membership'].keys()) - set(self.Meta.fields_membership):
                user_data['team_membership'].pop(key, None)
            profiles_serialized.append(user_data)
        return profiles_serialized

    def to_representation(self, instance):
        representation = serializers.ModelSerializer.to_representation(self, instance)
        if instance.curator:
            representation['curator'] = UserSerializer(instance.curator,
                                                       context={'request': self.context['request']},
                                                       fields=self.Meta.fields_curator).data
        return representation
