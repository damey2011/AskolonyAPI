from rest_framework import serializers

from Notification.models import Notification


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
