from django.db import models

# Create your models here.
from AskolonyAPI import settings

NOTIFICATION_TYPES = (
    ('NF', 'New Follower'),
    ('NC', 'New Comment'),
    ('NR', 'New Reply'),
    ('NU', 'New Upvote'),
    ('ND', 'New Downvote'),
    ('NM', 'New Milestone'),
    ('NM', 'New Post'),
)


class Notification(models.Model):
    note_type = models.CharField(choices=NOTIFICATION_TYPES, max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(default=1)
    thumbnail = models.ImageField(upload_to='notifications', default='/default/default_notification.png')
    read = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.note_type, self.owner.username)
