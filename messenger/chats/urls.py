from django.urls import path, re_path
from . import views

urlpatterns = [
    path("create_chat/", views.create_chat, name="create_chat"),
    path("get_chat/<int:chat_id>", views.get_chat, name="get_chat"),
    path("delete_chat/<int:chat_id>", views.delete_chat, name="delete_chat"),
    path("create_message/", views.create_message, name="create_message"),
    path("get_message/<int:message_id>", views.get_message, name="get_message"),
    path("get_user_chats/<int:user_id>", views.get_user_chats, name="get_user_chats"),
    path("get_messages_by_chat_and_user_id/", views.get_messages_by_chat_and_user_id,
         name="get_messages_by_chat_and_user_id"),
    path("update_notification_status_in_chat/<int:chat_id>",
         views.update_notification_status_in_chat,
         name="update_notification_status_in_chat"),
]
