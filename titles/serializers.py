from django.db.models import Avg
from rest_framework import serializers

from .models import Category, Genre, Title

class CategorySerializer(serializers.ModelSerializer):
    class Meta():
        fields = ['name', 'slug']
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta():
        fields = ['name', 'slug']
        model = Genre

# class RatingField(serializers.RelatedField):
#     def to_representation(self, obj):
#         avg = int(obj.reviews.aggregate(Avg('score')))
#         return 1 #avg

class TitleSerializer_post(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug', queryset=Genre.objects.all(), many=True)
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())

    class Meta():
        fields = '__all__'
        model = Title


class TitleSerializer_get(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta():

        fields = ['id', 'name', 'year', 'description', 'genre', 'category', 'rating']
        model = Title

    def get_rating(self, title):
        avg = title.reviews.aggregate(Avg('score'))
        return avg['score__avg']

