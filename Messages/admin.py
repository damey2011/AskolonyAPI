from django.contrib import admin

# Register your models here.
from Messages.models import Conversation, Message

admin.site.register(Conversation)
admin.site.register(Message)
