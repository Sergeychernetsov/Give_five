from django.contrib.auth import get_user_model
from django.db import models

QUESTION_CHOISES = (
    ('single', 'Единственный правильный ответ'),
    ('multiple', 'Несколько правильных ответов'),
    ('insertion', 'Ввод ответов через пробел'),
    ('correspond', 'Соотнесение вопросов и ответов'),
)

GRADE_CHOISES = (
    ('junior', '1-4 класс'),
    ('five', '5 класс'),
    ('six', '6 класс'),
    ('seven', '7 класс'),
    ('eight', '8 класс'),
    ('nine', '9 класс'),
    ('oge', 'ОГЭ'),
    ('ege', 'ЕГЭ'),
)

user = get_user_model()


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
    title = models.TextField(
        verbose_name='Текст вопроса. Если это вопрос на соотношение,'
                     'то в виде {"А": "текст вопроса 1", "Б": "текст вопроса 2"}',
        help_text='Введите текст вопроса',
    )
    multiple = models.CharField(
        verbose_name='Тип вопроса',
        help_text='Выберите тип вопроса',
        max_length=256,
        choices=QUESTION_CHOISES
    )
    theme = models.ForeignKey(
        'Theme',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    title = models.TextField(
        verbose_name='Ответ',
        help_text='Введите текст ответа. Если это вопрос на соотношение,'
                  ' то в виде {"1": "текст ответа 1", "2": "текст ответа 2"}',
    )
    is_right = models.BooleanField(
        verbose_name='Правильность',
        help_text='Отметьте, если ответ правильный',
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


class Theme(models.Model):
    title = models.CharField(
        verbose_name='Заголовок теста',
        help_text='Введите заголовок теста ',
        max_length=256,
    )
    description = models.TextField(
        verbose_name='Описание теста',
        help_text='Введите описания для данного теста',
    )
    theme_slug = models.SlugField(
        max_length=256,
        unique=True,
    )
    grade = models.ForeignKey(
        'Grade',
        on_delete=models.CASCADE,
        related_name='theme_test'
    )

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Grade(models.Model):
    level = models.CharField(
        verbose_name='Класс или Экзамен',
        help_text='Введите номер класса или аббревиатуру экзамены',
        choices=GRADE_CHOISES,
    )


class Result(models.Model):
    score = models.PositiveSmallIntegerField(
        verbose_name='Количество баллов'
    )
    finished_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата прохождения теста',
    )
    offer_course = models.BooleanField(
        verbose_name='Предложение курса',
        help_text='Предлагать курс только при плохом прохождении теста',
        default=False,
    )
    user = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
    )
    theme = models.ForeignKey(
        'Theme',
        on_delete=models.CASCADE,
    )
    monetization = models.ForeignKey(
        'Monetization',
        on_delete=models.PROTECT
    )

class Meta:
    # Если мы храним только последний пройденный тест для данного пользователя по данной теме
    constraints = [
        models.UniqueConstraint(
            fields=['user', 'theme'],
            name='user_passed_test'
        )
    ]
    verbose_name = 'Результат'
    verbose_name_plural = 'Результаты'
    ordering = ('finished_at',)
