from django.shortcuts import render
from rest_framework import filters, mixins, viewsets
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer)
from rest_framework.permissions import IsAdminUser
from .permissions import IsSuperuserPermission
from rest_framework.viewsets import GenericViewSet

from .models import Title, Genre, Category 


class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.DestroyModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsSuperuserPermission,)
    filterset_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.DestroyModelMixin, GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsSuperuserPermission,)
    filterset_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsSuperuserPermission,)
    filterset_fields = ['category', 'genre', 'name', 'year']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
