
from django.db import models
from django.conf import settings
# Create your models here.


class UserRegistrationModel(models.Model):
    user = models.OneToOneField(
        settings.auth_user_model, on_delete=models.CASCADE)