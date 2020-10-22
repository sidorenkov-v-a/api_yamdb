from django.shortcuts import render
from rest_framework import filters, mixins, viewsets

from .models import Title, Genre, Catigory 


class CatigoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.DestroyModelMixin, GenericViewSet):
    queryset = Catigory.obgects.all()
    serializer_class = 
    permission_classes = 
    filterset_fields = 

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.DestroyModelMixin, GenericViewSet):
    queryset = Genre.obgects.all()
    serializer_class = 
    permission_classes = 


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = 
    serializer_class = 
    permission_classes = 
    filterset_fields = ['category', 'genre', 'name', 'year']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
