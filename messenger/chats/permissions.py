from rest_framework import permissions

from chats.models import Chats


class IsChatCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user


class IsMessageAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user


class IsChatMember(permissions.BasePermission):
    def has_permission(self, request, view):
        chat_id = view.kwargs.get("chat_id")
        is_chat_member = Chats.objects.filter(id=chat_id, users__in=[request.user]).exists()
        return is_chat_member
