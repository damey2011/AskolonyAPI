from django.db import models
from AskolonyAPI import settings
from Post.models import Post
from Topic.models import Topic


class Poll(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_polls')
    title = models.CharField(max_length=200)
    description = models.TextField()
    assoc_post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    assoc_topic = models.ForeignKey(Topic, null=True, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    starts = models.DateTimeField()
    expires = models.DateTimeField()

    def __str__(self):
        return self.title

    def already_voted(self, user):
        return UserPolled.objects.filter(user=user, poll=self).exists()


class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    option = models.TextField()
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.poll.title + ' - ' + self.option


class UserPolled(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    poll_option = models.ForeignKey(PollOption, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s polled for %s' % (self.user.username, self.poll.title)
