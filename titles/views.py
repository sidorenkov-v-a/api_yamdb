from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet

from .filters import TitleFilter
from .models import Category, Genre, Title
from .permissions import IsSuperuserPermission
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer_get, TitleSerializer_post)


class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.DestroyModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsSuperuserPermission,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsSuperuserPermission,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsSuperuserPermission,)
    pagination_class = PageNumberPagination
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer_get
        return TitleSerializer_post
