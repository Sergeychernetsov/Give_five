from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from exams.models import Answer, Question, Theme
from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_exist(self, attrs):
        username = attrs.get('username')
        if_user = User.objects.filter(username=username)
        if if_user.exists():
            raise ValidationError('Пользователь с таким именем уже существует')
        email = attrs.get('email')
        if_email = User.objects.filter(email=email)
        if if_email.exists():
            raise ValidationError('Почта уже использовалась')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено.'
            )
        return value


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    phone_number = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
        )


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )


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
