from rest_framework import serializers

from Account.serializers import CreateUserSerializer
from Topic.models import Topic, TopicFollowing


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = (
            'id',
            'name',
            'description',
            'slug',
            'followers',
            'photo',
            'created',
            'created_by',
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


class TopicFollowSerializer(serializers.ModelSerializer):
    user = CreateUserSerializer(required=False)
    topic = TopicSerializer(required=False)

    class Meta:
        model = TopicFollowing
        fields = (
            'id',
            'user',
            'topic'
        )
