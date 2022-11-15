from django.urls import path

from users.views import UserAPIView

urlpatterns = [
    path("user/<int:pk>", UserAPIView.as_view()),
]