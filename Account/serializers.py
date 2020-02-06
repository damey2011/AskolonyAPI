import uuid

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from Account.models import UserProfile, UserStats, UserFollowings

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
    stats = GetUserStats(read_only=True)
    followers = serializers.IntegerField(read_only=True)
    followings = serializers.IntegerField(read_only=True)
    follows = serializers.SerializerMethodField(read_only=True)
    follows_you = serializers.SerializerMethodField(read_only=True)
    picture = serializers.ImageField(read_only=True, required=False)
    bio = serializers.CharField(read_only=True)

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
            'header_image',
            'picture',
            'followings',
            'followers',
            'profile',
            'stats',
            'follows',
            'follows_you',
            'topics_followed_count',
            'starred_posts_count',
            'website'
        )

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def update(self, instance, validated_data):
        print(validated_data)
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.username = validated_data.get('username', instance.username)
        instance.website = validated_data.get('website', instance.website)

        password = validated_data.pop('password', None)

        if password is not None and password != '':
            instance.set_password(validated_data.get('password'))

        instance.save()

        profile.college = profile_data.get('college', profile.college)
        profile.works = profile_data.get('works', profile.works)
        profile.lives = profile_data.get('lives', profile.lives)
        profile.facebook_link = profile_data.get('facebook_link', profile.facebook_link)
        profile.twitter_link = profile_data.get('twitter_link', profile.twitter_link)
        profile.linked_in_profile = profile_data.get('linked_in_profile', profile.linked_in_profile)
        profile.save()

        return instance

    def get_follows(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.is_following(request.user, obj)
        return False

    def get_follows_you(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.is_following(obj, request.user)
        return False


class SimpleNoEmailUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    follows = serializers.SerializerMethodField()
    follows_you = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'full_name',
            'picture',
            'header_image',
            'username',
            'bio',
            'follows',
            'follows_you'
        )

    def get_follows(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.is_following(request.user, obj)
        return False

    def get_follows_you(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.is_following(obj, request.user)
        return False


class FollowerSerializer(serializers.ModelSerializer):
    user = RetrieveUpdateDeleteUserSerializer()

    class Meta:
        model = UserFollowings
        fields = (
            'user',
        )

    def to_representation(self, instance):
        return SimpleNoEmailUserSerializer(instance.user, context=self.context).data


class FollowingSerializer(serializers.ModelSerializer):
    is_following = RetrieveUpdateDeleteUserSerializer()

    class Meta:
        model = UserFollowings
        fields = (
            'is_following',
        )

    def to_representation(self, instance):
        return SimpleNoEmailUserSerializer(instance.is_following, context=self.context).data


class UserNotificationSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'picture',
            'username',
        )


class UpdatePhotoSerializer(serializers.Serializer):
    picture = serializers.ImageField(allow_null=False)

    def to_representation(self, instance):
        return SimpleNoEmailUserSerializer(instance=instance).data
