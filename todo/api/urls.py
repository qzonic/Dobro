from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, TaskViewSet


router = DefaultRouter()
router.register('category', CategoryViewSet)
router.register('tasks', TaskViewSet, basename='tasks')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

