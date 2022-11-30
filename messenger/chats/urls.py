from django.urls import path, re_path
from . import views

urlpatterns = [
    path("create_chat/", views.create_chat, name="create_chat"),
    path("update_chat_name/<int:chat_id>", views.update_chat_name, name="update_chat_name"),
    path("update_chat_description/<int:chat_id>", views.update_chat_description, name="update_chat_description"),
    path("update_notification_status_in_chat/<int:chat_id>",
         views.update_notification_status_in_chat,
         name="update_notification_status_in_chat"),
    path("add_new_member_in_chat/<int:chat_id>", views.add_new_member_in_chat, name="add_new_member_in_chat"),
    path("delete_member_from_chat/<int:chat_id>", views.delete_member_from_chat, name="delete_member_from_chat"),
    path("delete_chat/<int:chat_id>", views.delete_chat, name="delete_chat"),
    path("get_chat/<int:chat_id>", views.get_chat, name="get_chat"),
    path("create_message/", views.create_message, name="create_message"),
    path("update_message_content/<int:message_id>", views.update_message_content, name="update_message_content"),
    path("update_message_status/<int:message_id>", views.update_message_status, name="update_message_status"),
    path("delete_message/<int:message_id>", views.delete_message, name="delete_message"),
    path("get_message/<int:message_id>", views.get_message, name="get_message"),
    path("get_chats_list_by_user_id/<int:user_id>",
         views.get_chats_list_by_user_id,
         name="get_chats_list_by_user_id"),
    path("get_all_messages_by_chat_id/<int:chat_id>",
         views.get_all_messages_by_chat_id,
         name="get_all_messages_by_chat_id"),
    path("get_info_about_user_by_id/<int:user_id>", views.get_info_about_user_by_id, name="get_info_about_user_by_id")
]
