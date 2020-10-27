from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import Comment, Review, Title, User


class ReviewSerializer(serializers.ModelSerializer):
    title = SlugRelatedField(slug_field='pk', read_only=True)
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    review = SlugRelatedField(slug_field='pk', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
