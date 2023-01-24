from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    GradeListModelViewSet,
    ThemeListModelViewSet,
)


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('index', GradeListModelViewSet)
router_v1.register(r'(?P<grade_level>\w+)', ThemeListModelViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
