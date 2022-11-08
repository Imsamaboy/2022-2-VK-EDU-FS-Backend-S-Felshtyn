import datetime

from django.db import models

from users.models import User


class Chats(models.Model):
    users = models.ManyToManyField(User,
                                   related_name='chat_user',
                                   verbose_name="Собеседники")

    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name="Дата создания",
                                        null=False)

    mute_notifications = models.BooleanField(verbose_name="Уведомления",
                                             default=False,
                                             null=False)

    chat_name = models.TextField(verbose_name="Название чата",
                                 null=False)

    chat_description = models.TextField(verbose_name="Описание",
                                        null=False)

    def __str__(self):
        return f"""
        id: {self.id}, 
        users: {self.users}, 
        chat_name: {self.chat_name}, 
        chat_description: {self.chat_description}
        """

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class Message(models.Model):
    chat = models.ForeignKey(Chats,
                             on_delete=models.CASCADE,
                             null=False,
                             verbose_name="Чат")

    sender = models.ForeignKey(User, on_delete=models.SET_NULL,
                               null=True,
                               related_name='sender',
                               verbose_name="Отправитель")

    message = models.TextField(verbose_name="Сообщение")

    send_time = models.DateTimeField(auto_now_add=True,
                                     verbose_name="Время отправления")

    is_read = models.BooleanField(default=False,
                                  null=False,
                                  verbose_name="Прочитано")

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
