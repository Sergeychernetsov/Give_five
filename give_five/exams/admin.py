from django.contrib import admin

from .models import Theme, Answer, Question, Grade, Result


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"theme_slug": ("theme_title",)}
    list_display = ('id', 'theme_title', 'grade')


class AnswerInline(admin.TabularInline):
    model = Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = (AnswerInline,)
    list_display = ('id', 'theme', 'question_type', 'question_title')


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'level',)
    list_editable = ('level',)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'score', 'offer_course', 'finished_at')

# TODO подправить название Grade  в админке Тестов на человекочитаемое
