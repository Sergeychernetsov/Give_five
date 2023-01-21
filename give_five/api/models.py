from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import User


class Theme(models.Model):
    title = models.CharField(max_length=100, verbose_name='Названиие темы экзамена')
    description = models.CharField(max_length=255, verbose_name='Описание темы')


class Monetization(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    # payment =


class Result(models.Model):
    theme = models.ForeignKey(
        Theme,
        related_name='results',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name='results',
        on_delete=models.CASCADE,
    )
    score = models.IntegerField(verbose_name='Оценка',
                                validators=(MinValueValidator(1),
                                            MaxValueValidator(100)))

    pub_date = models.DateTimeField(verbose_name='Дата прохождения теста',
                                    auto_now=True)
    monetization = models.ForeignKey(
        'Monetization',
        on_delete=models.CASCADE,

    )

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'
