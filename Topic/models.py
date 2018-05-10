from django.db import models

# Create your models here.
from django.utils.text import slugify

from AskolonyAPI import settings
from Post.models import PostTopic


class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    slug = models.SlugField(max_length=100)
    header_image = models.ImageField(upload_to='topics-header-images', default='/default/post-header.png')
    photo = models.ImageField(upload_to='topics', default='/default/user.png')
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def posts_count(self):
        return PostTopic.objects.filter(topic=self).count()

    def get_follows(self, user):
        if user.is_authenticated:
            return TopicFollowing.objects.filter(user=user).exists()
        return False

    def followers(self):
        return TopicFollowing.objects.filter(topic=self).count()

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
