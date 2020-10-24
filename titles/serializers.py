from rest_framework import serializers

from titles.models import Title, Category, Genre


class CategorySerializer(serializers.ModelSerializer):


    class Meta():
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):


    class Meta():
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):


    class Meta():
        fields = '__all__'
        model = Title
