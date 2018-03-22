from rest_framework import serializers

from Account.serializers import CreateUserSerializer
from Poll.models import Poll, PollOption
from Post.models import Post
from Post.serializers import RetrieveUpdateDestroyPostSerializer
from Topic.models import Topic
from Topic.serializers import TopicSerializer


class PollOptionSerializer(serializers.ModelSerializer):
    # votes = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = PollOption
        fields = (
            'id',
            'option',
            'votes'
        )
        extra_kwargs = {
            'votes': {
                'read_only': True,
                'required': False
            },
        }


class PollSerializer(serializers.ModelSerializer):
    assoc_post = RetrieveUpdateDestroyPostSerializer(read_only=True)
    assoc_post_id = serializers.PrimaryKeyRelatedField(source='assoc_post', queryset=Post.objects.all(), required=False, write_only=True)
    assoc_topic = TopicSerializer(read_only=True)
    assoc_topic_id = serializers.PrimaryKeyRelatedField(source='assoc_topic', queryset=Topic.objects.all(), required=False, write_only=True)
    user = CreateUserSerializer(required=False)
    options = PollOptionSerializer(many=True)

    class Meta:
        model = Poll
        fields = (
            'id',
            'title',
            'description',
            'assoc_post',
            'assoc_post_id',
            'assoc_topic',
            'assoc_topic_id',
            'is_public',
            'created',
            'starts',
            'expires',
            'user',
            'options'
        )

    def create(self, validated_data):
        options = validated_data.pop('options')
        p = Poll.objects.create(**validated_data)
        for option in options:
            PollOption.objects.create(poll=p, **option)
        return p
