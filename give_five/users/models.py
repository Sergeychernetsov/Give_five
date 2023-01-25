from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=100,
                              verbose_name='Email',
                              help_text='Укажите email',
                              unique=True,
                              )
    phone_number = models.IntegerField(blank=True,
                                       verbose_name='Телефон',
                                       help_text='Укажите номер телефона',
                                       null=True,
                                       )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return self.email
