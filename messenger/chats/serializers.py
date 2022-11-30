from rest_framework import serializers

from chats.models import Chats, Message


class ChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chats
        fields = ('id', 'chat_name', 'chat_description', 'mute_notifications', 'created_date', 'users', 'creator')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'message', 'send_time', 'is_read', 'sender', 'chat')
