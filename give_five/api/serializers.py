from rest_framework import serializers

from exams.models import Grade, Theme, Question, Answer


class GradeListSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()

    class Meta:
        model = Grade
        fields = ('id', 'level',)

    def get_level(self, obj):
        """Отображение level в человекочитаемом виде."""
        return obj.get_level_display()


class ThemeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ('id', 'theme_title',)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'answer_title')


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'question_title', 'question_type', 'answers')


class ThemeDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Theme
        fields = ('id', 'theme_title', 'theme_slug', 'questions')
        lookup_field = 'theme_slug'
