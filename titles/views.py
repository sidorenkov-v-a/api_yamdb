from django.shortcuts import render
from rest_framework import filters, mixins, viewsets
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer)
from rest_framework.permissions import IsAdminUser
from .permissions import IsSuperuserPermission
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import PageNumberPagination

from .models import Title, Genre, Category 


class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.DestroyModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsSuperuserPermission,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]
    lookup_field = 'slug'

class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.DestroyModelMixin, GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsSuperuserPermission,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsSuperuserPermission,)
    pagination_class = PageNumberPagination
    filterset_fields = ['category', 'genre', 'name', 'year']
    lookup_field = 'slug'

