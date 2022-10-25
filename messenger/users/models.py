from django.db import models


# Create your models here.
class Users(models.Model):
    login = models.CharField(max_length=15, null=False)
    first_name = models.CharField(max_length=40, null=False)
    last_name = models.CharField(max_length=40, null=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100)
