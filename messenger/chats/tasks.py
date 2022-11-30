from django.core.mail import send_mail

from application.celery import app
from application.settings import ADMINS, EMAIL_HOST_USER


@app.task()
def send_admin_email(recipient_list):
    """
    :return:
    """
    send_mail(
        subject="New chat created",
        message="Hey! New chat created!",
        from_email=EMAIL_HOST_USER,
        recipient_list=recipient_list
    )
