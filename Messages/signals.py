from django.db.models.signals import post_save
from django.dispatch import receiver

from Account.serializers import UserNotificationSerializer
from Messages.models import Message
from Messages.serializers import MessageNotificationSerializer
from Notification.tasks import createNotification


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance=None, created=False, **kwargs):
    if created:
        owner = instance.recipient
        sender = instance.sender

        actor = UserNotificationSerializer(sender).data
        target = MessageNotificationSerializer(instance).data

        """Async Create Notification Here"""
        createNotification.delay(str(owner.id), actor, "sent", target=target)
