from django.db import models

# Create your models here.
from django.utils.text import slugify

from AskolonyAPI import settings


class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    slug = models.SlugField(max_length=100)
    followers = models.PositiveIntegerField(default=0)
    photo = models.ImageField(upload_to='topics', default='/default/post-header.png')
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Topic, self).save(*args, **kwargs)


class TopicFollowing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.user.first_name + ' FOLLOWS ' + self.topic.name
