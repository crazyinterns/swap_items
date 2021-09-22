from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    """кастомный пользователь системы """
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
        null=True
    )
    phonenumber = PhoneNumberField(
        verbose_name="Мобильный номер"
    )
    other_contact = models.CharField(
        'Прочий контакт',
        max_length=100,
        blank=True,
    )
    objects = UserManager()

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f"{self.get_full_name}"
