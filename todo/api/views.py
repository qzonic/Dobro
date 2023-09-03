from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .mixins import ListCreateViewSet
from .permissions import IsOwner
from .filters import TaskFilter


class CategoryViewSet(ListCreateViewSet):
    """ Viewset that provides `GET` and `POST` methods. """

    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TaskViewSet(viewsets.ModelViewSet):
    """
    Viewset that provides `GET`, `POST`, `PUT`, `PATCH` and `DELETE` methods.
    """

    permission_classes = (IsOwner,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter

    def get_queryset(self):
        return self.request.user.tasks.all()

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx
