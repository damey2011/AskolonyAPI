from rest_framework import serializers

from Account.serializers import CreateUserSerializer
from Poll.models import Poll
from Post.serializers import RetrieveUpdateDestroyPostSerializer
from Topic.serializers import TopicSerializer


class PollSerializer(serializers.ModelSerializer):
    assoc_post = RetrieveUpdateDestroyPostSerializer(required=False)
    assoc_topic = TopicSerializer(required=False)
    user = CreateUserSerializer(required=False)

    class Meta:
        model = Poll
        fields = (
            'id',
            'title',
            'description',
            'assoc_post',
            'created',
            'starts',
            'expires',
            'user'
        )
