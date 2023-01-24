from rest_framework.viewsets import ModelViewSet

from exams.models import Grade, Theme
from .serializers import (
    GradeListSerializer,
    ThemeListSerializer,
    ThemeDetailSerializer,
)


class GradeListModelViewSet(ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeListSerializer


class ThemeListModelViewSet(ModelViewSet):
    queryset = Theme.objects.all()
    lookup_field = 'theme_slug'

    def get_queryset(self):
        theme_slug = self.kwargs.get('theme_slug', None)
        grade_slug = self.kwargs.get('grade_level')
        if theme_slug:
            theme = Theme.objects.filter(theme_slug=theme_slug)
            for question in theme[0].questions.all():
                if question.question_type == 'insertion':
                    for answer in question.answers.all():
                        answer.delete()
            return theme
        else:
            return Theme.objects.filter(grade__level=grade_slug)

    def get_serializer_class(self):
        if self.kwargs.get('theme_slug', None):
            return ThemeDetailSerializer
        return ThemeListSerializer
