# Generated by Django 3.2 on 2023-01-22 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500, verbose_name='Тело ответа')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Тело вопроса')),
                ('type', models.CharField(choices=[('one_answer', 'Единственный возможный ответ'), ('many_answers', 'Множество возможных ответов'), ('string_answer', 'Строчный ввод'), ('corresp_answer', 'Таблица соответствия')], default='one_answer', max_length=100, verbose_name='Тип вопроса')),
                ('correct_answer', models.CharField(max_length=1000, verbose_name='Строка с правильным ответом')),
                ('answers', models.ManyToManyField(blank=True, to='exams.Answer', verbose_name='Список возможных ответов')),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Названиие темы экзамена')),
                ('description', models.CharField(max_length=255, verbose_name='Описание темы')),
                ('questions', models.ManyToManyField(blank=True, to='exams.Question', verbose_name='Список вопросов')),
            ],
        ),
    ]