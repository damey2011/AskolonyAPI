import uuid

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from Account.models import UserProfile, UserStats

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
            'username',
        )

        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'username': {
                'required': False
            },
            'first_name': {
                'required': False
            },
            'last_name': {
                'required': False
            }
        }

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        if email is None:
            raise ValidationError('Email field may not be empty')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email has been taken')
        if len(password) < 6 or password is None:
            raise ValidationError('Password should be 6 characters or more')

        return attrs

    def create(self, validated_data):
        email = validated_data.get('email', None)
        password = validated_data.get('password', None)
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')
        username = validated_data.get('username', str(uuid.uuid4())[:10])

        user = User.objects.create(email=email, first_name=first_name, last_name=last_name, username=username)
        user.set_password(password)
        user.save()

        return user


class GetUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'college',
            'works',
            'lives',
            'facebook_link',
            'twitter_link',
            'linked_in_profile'
        )


class GetUserStats(serializers.ModelSerializer):
    class Meta:
        model = UserStats
        fields = (
            'reads',
            'comments',
            'writes',
            'ups',
            'downs'
        )


class RetrieveUpdateDeleteUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    profile = GetUserProfileSerializer()
    stats = GetUserStats()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'password',
            'username',
            'bio',
            'picture',
            'followings',
            'followers',
            'profile',
            'stats'
        )

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.username = validated_data.get('username', instance.username)
        instance.save()

        profile.college = profile_data.get('college', profile.college)
        profile.works = profile_data.get('works', profile.works)
        profile.lives = profile_data.get('lives', profile.lives)
        profile.facebook_link = profile_data.get('facebook_link', profile.facebook_link)
        profile.twitter_link = profile_data.get('twitter_link', profile.twitter_link)
        profile.linked_in_profile = profile_data.get('linked_in_profile', profile.linked_in_profile)
        profile.save()

        return instance
