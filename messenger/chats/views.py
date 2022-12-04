from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from chats.models import Chats, Message
from chats.permissions import IsChatCreator, IsChatMember
from chats.serializers import ChatsSerializer, MessageSerializer
from chats.tasks import send_admin_email


class ChatsListView(generics.ListCreateAPIView):
    serializer_class = ChatsSerializer
    permission_classes = [IsAuthenticated]
    queryset = Chats.objects.all()
    lookup_url_kwarg = "user_id"


class ChatDeleteEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatsSerializer
    # queryset = Chats.objects.all()
    lookup_url_kwarg = "chat_id"

    def get_queryset(self):
        return Chats.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg))

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            permission_classes = [IsAuthenticated, IsChatCreator]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_update(self, serializer):
        serializer.save()
        send_admin_email.delay([self.get_queryset().first().creator.email])


class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsChatMember]
    queryset = Message.objects.all()
    lookup_url_kwarg = "chat_id"


class MessageDeleteEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated, IsChatMember, IsChatCreator]
