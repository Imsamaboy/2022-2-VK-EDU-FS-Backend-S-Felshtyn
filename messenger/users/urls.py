from django.urls import path, re_path

from users import views
from users.views import UserAPIView

urlpatterns = [
    path("user/<int:pk>", UserAPIView.as_view()),
]