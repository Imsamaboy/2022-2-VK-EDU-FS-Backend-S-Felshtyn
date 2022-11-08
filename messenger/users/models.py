from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.TextField(verbose_name="Номер телефона",
                                    blank=True)
    last_seen_at = models.DateTimeField(verbose_name="Дата последнего посещения ресурса",
                                        auto_now=True)
    description = models.CharField(max_length=100,
                                   verbose_name="Описание профиля")

    def __str__(self):
        return f"""
        username: {self.username}, 
        email: {self.email},
        phone: {self.phone_number}
        """

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
