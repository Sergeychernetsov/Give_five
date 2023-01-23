from django.db import models


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
