from django.db import models


QUESTION_TYPES = (
    ('one_answer', 'Единственный возможный ответ'),
    ('many_answers', 'Множество возможных ответов'),
    ('string_answer', 'Строчный ввод'),
    ('corresp_answer', 'Таблица соответствия')
)


class Answer(models.Model):
    text = models.CharField(
        max_length=500,
        verbose_name='Тело ответа'
    )


# оставляю m2m отношения с параметрами null/blank=True и дефолтные значения
# для простоты создания тестового контента
class Question(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Тело вопроса'
    )
    type = models.CharField(
        max_length=100,
        verbose_name='Тип вопроса',
        choices=QUESTION_TYPES,
        default='one_answer'
    )
    answers = models.ManyToManyField(
        Answer,
        blank=True,
        verbose_name='Список возможных ответов'
    )
    correct_answer = models.CharField(
        max_length=1000,
        verbose_name='Строка с правильным ответом'
    )


# оставляю m2m отношения с параметрами null/blank=True и дефолтные значения
# для простоты создания тестового контента
class Theme(models.Model):
    title = models.CharField(max_length=100, verbose_name='Названиие темы экзамена')
    description = models.CharField(max_length=255, verbose_name='Описание темы')
    questions = models.ManyToManyField(
        Question,
        blank=True,
        verbose_name='Список вопросов'
    )


