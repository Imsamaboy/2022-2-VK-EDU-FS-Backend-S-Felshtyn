from django.urls import path
from .views import MessageDeleteEditView, MessageListView, ChatDeleteEditView, ChatsListView

urlpatterns = [
    path("message/<int:pk>/", MessageDeleteEditView.as_view()),
    path("chat_messages/<int:chat_id>/", MessageListView.as_view()),
    path("<int:pk>/", ChatDeleteEditView.as_view()),
    path("users/<int:user_id>/", ChatsListView.as_view())
]
