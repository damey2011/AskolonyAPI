from django.db import models


# Create your models here.
from django.urls import reverse
from django.utils.text import slugify

from AskolonyAPI import settings


class Question(models.Model):
    title = models.CharField(max_length=750)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='my_questions')
    body = models.TextField(blank=True)
    followings = models.IntegerField(default=0)
    answers = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=100, unique=True, null=True)
    is_anonymous = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created", "-title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Question, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('get-question', kwargs={"pk": self.pk})


class QuestionFollowing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followed_questions")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="followers")
    created = models.DateTimeField(auto_now_add=True)
