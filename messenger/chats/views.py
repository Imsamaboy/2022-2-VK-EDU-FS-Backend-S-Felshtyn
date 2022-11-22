from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from chats.models import Chats, Message
from chats.serializers import ChatsSerializer, MessageSerializer


class ChatsListView(generics.ListCreateAPIView):
    serializer_class = ChatsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Chats.objects.filter(user=user_id)


class ChatDeleteEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatsSerializer
    queryset = Chats.objects.all()
    permission_classes = [IsAuthenticated]


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


def login(request):
    return render(request, 'login.html')
