from rest_framework import serializers

from Notification.models import Notification, NotificationCass


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id',
            'note_type',
            'object_ref',
            'object_type',
            'text',
            'thumbnail',
            'read',
            'created'
        )

        # def to_representation(self, instance):
        #     pass


class NotificationCassSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    note_type = serializers.CharField()
    owner = serializers.CharField()
    actor = serializers.DictField()
    verb = serializers.CharField()
    action_object = serializers.DictField()
    target = serializers.DictField()
    read = serializers.BooleanField()
    created = serializers.DateTimeField()

    class Meta:
        model = NotificationCass
        fields = "__all__"
