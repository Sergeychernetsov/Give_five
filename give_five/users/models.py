from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username


class Documentation(models.Model):
    """Модель, в которой хранится пара ключ-значение.

     Значения используются на сайте в разных местах."""
    key = models.CharField(
        verbose_name='ключ',
        help_text='Введите ключ, который будет использоваться на сайте.',
        max_length=256,
        )
    description = models.TextField(
        verbose_name='значение',
        help_text='Введите текст, который будет отображаться на сайте.',
    )

    class Meta:
        ordering = ('key',)
        verbose_name = 'Текст с сайта'
        verbose_name_plural = 'Текста с сайта'


class Question(models.Model):
    title = models.CharField(
        verbose_name='Текст вопроса. Если это вопрос на соотношение,'
                     'то в виде {"А": "текст вопроса 1", "Б": "текст вопроса 2"}',
        help_text='Введите текст вопроса',
        max_length=256,
    )
    multiple = models.BooleanField(
        verbose_name='Множественный выбор',
        help_text='Выберите, если у вопроса несколько правильных ответов',
        default=False,
    )
    correspond = models.BooleanField(
        verbose_name='Соотнешение',
        help_text='Выберите, если это вопрос на соотношение вопрос-ответ',
        default=False,
    )
    theme = models.ForeignKey(
        'Theme',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    title = models.CharField(
        verbose_name='Ответ',
        help_text='Введите текст ответа. Если это вопрос на соотношение,'
                  ' то в виде {"1": "текст ответа 1", "2": "текст ответа 2"}',
        max_length=256,
    )
    is_right = models.BooleanField(
        verbose_name='Правильность',
        help_text='Правильный ли ответ',
        default=False,
    )
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
    )
    correspond_answer = models.TextField(
        verbose_name='Словарь правильных ответов',
        help_text='Введите правильные ответы на вопросы в виде { "А": "1", "Б": "3"}',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
