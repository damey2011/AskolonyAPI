from django.contrib import admin

# Register your models here.
from Poll.models import Poll, PollOption, UserPolled

admin.site.register(Poll)
admin.site.register(PollOption)
admin.site.register(UserPolled)
