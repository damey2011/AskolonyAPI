from django.contrib.auth import get_user_model
from rest_framework import serializers

from Account.serializers import SimpleNoEmailUserSerializer
from Messages.models import Message, Conversation


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'


class MessageThreadSerializer(serializers.ModelSerializer):
    sender = SimpleNoEmailUserSerializer(read_only=True)
    recipient = SimpleNoEmailUserSerializer(read_only=True)
    conversation = ConversationSerializer(read_only=True)

    class Meta:
        model = Message
        fields = (
            'id',
            'conversation',
            'recipient',
            'text',
            'sender',
            'read',
            'created'
        )


User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    conversation = ConversationSerializer(required=False, read_only=True)
    recipient = SimpleNoEmailUserSerializer(read_only=True)
    sender = SimpleNoEmailUserSerializer(read_only=True)
    read = serializers.BooleanField(read_only=True)

    class Meta:
        model = Message
        fields = (
            'id',
            'conversation',
            'recipient',
            'text',
            'sender',
            'read',
            'created'
        )


class MessageNotificationSerializer(serializers.ModelSerializer):
    conversation = serializers.CharField(read_only=True)

    class Meta:
        model = Message
        fields = (
            'conversation',
            'text',
        )
