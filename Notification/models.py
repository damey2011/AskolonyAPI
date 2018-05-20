import uuid

import datetime
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from django_cassandra_engine.models import DjangoCassandraModel, columns

from Account.models import UserFollowings
from AskolonyAPI import settings
from Messages.models import Message

NOTIFICATION_TYPES = (
    ('NF', 'New Follower'),
    ('NC', 'New Comment'),
    ('NM', 'New Message'),
    ('NR', 'New Reply'),
    ('NU', 'New Upvote'),
    ('ND', 'New Downvote'),
    ('NM', 'New Milestone'),
    ('NM', 'New Post'),
)

OBJECT_TYPES = (
    ('P', 'Post'),
    ('U', 'User'),
    ('T', 'Topic'),
    ('C', 'Comment'),
    ('M', 'Message'),
)


class Notification(models.Model):
    note_type = models.CharField(choices=NOTIFICATION_TYPES, max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    object_ref = models.CharField(null=True, blank=True, max_length=100)
    object_type = models.CharField(choices=OBJECT_TYPES, max_length=100)
    text = models.TextField()
    thumbnail = models.ImageField(upload_to='notifications', default='/default/default_notification.png')
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.note_type, self.owner.username)


"""Post save signals that will create notifications"""


@receiver(post_save, sender=UserFollowings)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        owner = instance.is_following
        ref = instance.user
        Notification.objects.create(note_type='NF',
                                    owner=owner,
                                    object_ref=ref.username,
                                    object_type='U',
                                    text='%s started following you' % ref.get_full_name(),
                                    thumbnail=ref.picture)


class NotificationCass(DjangoCassandraModel):
    id = columns.UUID(primary_key=True, default=uuid.uuid4())
    note_type = columns.Text(max_length=50, primary_key=True)
    owner = columns.Integer(primary_key=True)
    actor = columns.Map(key_type=columns.Text(), value_type=columns.Text())
    verb = columns.Text()
    action_object = columns.Map(key_type=columns.Text(), value_type=columns.Text(), default=None)
    target = columns.Map(key_type=columns.Text(), value_type=columns.Text())
    read = columns.Boolean(default=False)
    created = columns.DateTime(default=datetime.datetime.now())

    class Meta:
        get_pk_field = 'id'
