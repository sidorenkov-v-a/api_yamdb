from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField
from titles.models import Title, Category, Genre
from django.db.models import Avg
from reviews.models import Review

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

class TitleSerializer(serializers.ModelSerializer):

    genre = SlugRelatedField(slug_field='slug', read_only=True)
    category = SlugRelatedField(slug_field='slug', read_only=True)
    #rating = RatingField(read_only=True)
    rating = serializers.SerializerMethodField()
    def get_rating(self, title):
        avg = title.reviews.aggregate(Avg('score'))
        return avg['score__avg']
        
   

    class Meta():

        fields = ['id', 'name', 'year', 'description', 'genre', 'category', 'rating']
        model = Title


