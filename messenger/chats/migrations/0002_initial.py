# Generated by Django 4.1.2 on 2022-11-01 19:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='recipient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipient', to=settings.AUTH_USER_MODEL, verbose_name='Получатель'),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель'),
        ),
        migrations.AddField(
            model_name='chats',
            name='first_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chat_first_user_name', to=settings.AUTH_USER_MODEL, verbose_name='Собеседник 1'),
        ),
        migrations.AddField(
            model_name='chats',
            name='second_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chat_second_user_name', to=settings.AUTH_USER_MODEL, verbose_name='Собеседник 2'),
        ),
    ]
