from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField

from titles.models import Title

from .models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review
        extra_kwargs = {'title': {'required': False}}

    def validate(self, data):
        request = self.context.get('request')
        title_id = request.parser_context.get('kwargs').get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST' and
            Review.objects.filter(title=title, author=request.user).exists()
        ):
            raise serializers.ValidationError('ValidationError')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        extra_kwargs = {'review': {'required': False}}
