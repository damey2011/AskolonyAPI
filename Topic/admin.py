from django.contrib import admin

# Register your models here.
from Topic.models import Topic, TopicFollowing

admin.site.register(Topic)
admin.site.register(TopicFollowing)
