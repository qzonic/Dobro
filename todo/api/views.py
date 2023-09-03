from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .mixins import ListCreateViewSet
from .permissions import IsOwner
from .filters import TaskFilter
from .serializers import (
    CategorySerializer,
    TaskCreateSerializer,
    TaskReadSerializer,
)
from main.models import Category


class CategoryViewSet(ListCreateViewSet):
    """ Viewset that provides `GET` and `POST` methods. """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'id',)


class TaskViewSet(viewsets.ModelViewSet):
    """
    Viewset that provides `GET`, `POST`, `PUT`, `PATCH` and `DELETE` methods.
    """

    permission_classes = (IsOwner,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter

    def get_queryset(self):
        return self.request.user.tasks.all()

    # def get_serializer_context(self):
    #     ctx = super().get_serializer_context()
    #     ctx['request'] = self.request
    #     return ctx

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return TaskReadSerializer
        return TaskCreateSerializer
