from django.db import models

from users.models import User


class Chats(models.Model):
    first_user = models.ForeignKey(User,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='chat_first_user_name',
                                   verbose_name="Собеседник 1")

    second_user = models.ForeignKey(User, on_delete=models.SET_NULL,
                                    null=True,
                                    related_name='chat_second_user_name',
                                    verbose_name="Собеседник 2")

    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name="Дата создания")

    mute_notifications = models.BooleanField(null=False, verbose_name="Уведомления")

    def __str__(self):
        return f"id: {self.id}, user_1: {self.first_user}, user_2: {self.second_user}"

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

    recipient = models.ForeignKey(User,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  related_name='recipient',
                                  verbose_name="Получатель")
    message = models.TextField(verbose_name="Сообщение")
    send_time = models.DateTimeField(auto_now_add=True, verbose_name="Время отправления")

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
