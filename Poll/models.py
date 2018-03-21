from django.db import models

# Create your models here.
from AskolonyAPI import settings
from Post.models import Post
from Topic.models import Topic


class Poll(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_polls')
    title = models.CharField(max_length=200)
    description = models.TextField()
    assoc_post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    assoc_topic = models.ForeignKey(Topic, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    starts = models.DateTimeField()
    expires = models.DateTimeField()

    def __str__(self):
        return self.title


class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    option = models.TextField()
    votes = models.PositiveIntegerField()

    def __str__(self):
        return self.poll.title + ' - ' + self.option


class UserPolled(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return '%s polled for %s' % (self.user.username, self.poll.title)
