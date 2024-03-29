from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=100,
                              verbose_name='Email',
                              help_text='Укажите email',
                              unique=True,
                              null=False)
    phone_number = models.IntegerField(blank=True,
                                       verbose_name='Телефона',
                                       help_text='Укажите номер телефона')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
