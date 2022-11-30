from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from chats.models import Chats, Message
from chats.serializers import ChatsSerializer, MessageSerializer
from chats.tasks import send_admin_email
from users.models import User


class ChatsListView(generics.ListCreateAPIView):
    serializer_class = ChatsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Chats.objects.filter(users=user_id)


class ChatDeleteEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs["pk"]
        return Chats.objects.filter(id=chat_id)

    def perform_update(self, serializer):
        serializer.save()
        chat = self.get_queryset().first()
        send_admin_email.delay(recipient_list=[chat.creator.email])


class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs["chat_id"]
        return Message.objects.filter(chat=chat_id)


class MessageDeleteEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]

