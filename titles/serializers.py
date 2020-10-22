from rest_framework import serializers

from .models import Catigory, Genre, Title


class CatigorySerializer(serializers.ModelSetializer):


    class Meta():
        fields = '__all__'
        model = Catigory


class GenreSerializer(serializers.ModelSetializer):


    class Meta():
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSetializer):


    class Meta():
        fields = '__all__'
        model = Title
