from django.contrib import admin

from chats.models import Message, Chats

admin.site.register(Message)
admin.site.register(Chats)
