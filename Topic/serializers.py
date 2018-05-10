from rest_framework import serializers

from Account.serializers import CreateUserSerializer, SimpleNoEmailUserSerializer
from Post.models import PostTopic
from Post.serializers import RetrieveUpdateDestroyPostSerializer
from Topic.models import Topic, TopicFollowing


class TopicSerializer(serializers.ModelSerializer):
    followers = serializers.IntegerField(read_only=True)
    photo = serializers.ImageField(required=False)
    posts_count = serializers.IntegerField(read_only=True)
    follows = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Topic
        fields = (
            'id',
            'name',
            'description',
            'slug',
            'followers',
            'header_image',
            'photo',
            'created',
            'created_by',
            'posts_count',
            'follows',
            'updated'
        )
        extra_kwargs = {
            'slug': {
                'read_only': True
            },
            'created_by': {
                'read_only': True
            }
        }

    def get_follows(self, obj):
        request = self.context.get('request', None)
        if request:
            return obj.get_follows(self.context['request'].user)
        else:
            return False


class TopicFollowSerializer(serializers.ModelSerializer):
    user = CreateUserSerializer(required=False)
    topic = TopicSerializer(required=False)

    class Meta:
        model = TopicFollowing
        fields = (
            'user',
            'topic'
        )

    def to_representation(self, instance):
        return SimpleNoEmailUserSerializer(instance.user, context=self.context).data


class TopicFollowedByUserSerializer(serializers.ModelSerializer):
    topic = TopicSerializer()

    class Meta:
        model = TopicFollowing
        fields = (
            'topic'
        )


class TopicPostSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(required=False)
    created_by = CreateUserSerializer(required=False)

    class Meta:
        model = PostTopic
        fields = (
            'created_by',
            'topic',
            'post'
        )

    def to_representation(self, instance):
        return RetrieveUpdateDestroyPostSerializer(instance.post, context=self.context).data
