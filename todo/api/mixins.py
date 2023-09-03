from rest_framework import mixins, viewsets


class ListCreateViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """ A viewset that provides default `create()` and `list()` actions. """
    pass
