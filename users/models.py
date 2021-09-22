from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUser(AbstractUser):
    """кастомный пользователь системы """
    objects = UserManager()

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f"{self.get_full_name}"
