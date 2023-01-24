from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from exams.models import Question, Theme
from give_five import settings
from users.models import User
from .email import send_confirmation_code
from .serializers import QuestionSerializer, QuestionCheckSerializer, ThemeSerializer, \
    AdminUserSerializer, SignUpSerializer, TokenSerializer


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


class ConfCodeView(APIView):
    """
    При получении POST-запроса с email и username отправляет
    письмо с confirmation_code на email.
    """

    # permission_classes =

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email = serializer.validated_data.get('email')
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения регистрации',
            message='Вы зарегистрировались на учебной платформе "Дай 5!"'
                    f'Ваш код подтвержения: {confirmation_code}',
            from_email=settings.ADMIN_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TokenView(APIView):
    """
    При получении POST-запроса с username и confirmation_code
    возвращает JWT-токен.
    """

    # permission_classes =

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        username = serializer.data['username']
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.data['confirmation_code']
        if not default_token_generator.check_token(user, confirmation_code):
            return Response({'Неверный код'},
                            status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken.for_user(user)
        return Response({'token': token.access_token},
                        status=status.HTTP_200_OK)


class UserRegView(APIView):
    # permission_classes =

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_confirmation_code(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    # permission_classes =
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    lookup_value_regex = r'[\w\@\.\+\-]+'
    search_fields = ('username',)
