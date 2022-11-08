from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.get_chats_list, name='get_chats_list'),
    path("create/", views.create_chat, name='create_chat'),
    path("chat/<int:id>/", views.get_chat_page, name='get_chat_page'),
]