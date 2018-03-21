from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model

from Account.models import UserStats, UserProfile, UserFollowings

User = get_user_model()

admin.site.register(User)
admin.site.register(UserStats)
admin.site.register(UserProfile)
admin.site.register(UserFollowings)
