from rest_framework import serializers

from exams.models import Answer, Question, Theme


class AnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    text = serializers.CharField()

    class Meta:
        model = Answer
        fields = ('id', 'text',)


class QuestionSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'title', 'answers')


class ThemeSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField()
    # questions = QuestionSerializer(many=True) - если нужно выводить вложенным объектом
    questions = serializers.SerializerMethodField(source='get_questions')

    def get_questions(self, instance):
        id_list = []
        for obj in instance.questions.all().values('id'):
            id_list.append(obj)
        return id_list

    class Meta:
        model = Theme
        fields = ('title', 'description', 'questions')


class QuestionCheckSerializer(serializers.ModelSerializer):
    correct_answer = serializers.CharField(required=True)

    class Meta:
        model = Question
        fields = ('id', 'correct_answer')