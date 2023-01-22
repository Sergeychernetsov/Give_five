from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from exams.models import Answer, Question, Theme
from .serializers import AnswerSerializer, QuestionSerializer, QuestionCheckSerializer, ThemeSerializer


class ThemeViewset(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer


class QuestionViewset(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_serializer_class(self):
        if self.action == 'check':
            return QuestionCheckSerializer
        return QuestionSerializer

    @action(methods=('post',), detail=True)
    def check(self, request, pk):
        instance = get_object_or_404(Question, pk=pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        attempt = serializer.data.get('correct_answer')
        if attempt == instance.correct_answer:
            return Response(
                'Правильный ответ',
                status=status.HTTP_200_OK
            )
        return Response(
            'Неправильный ответ',
            status=status.HTTP_200_OK
        )
