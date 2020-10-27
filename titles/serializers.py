from rest_framework import serializers

from .models import Title, Category, Genre


class CategorySerializer(serializers.ModelSerializer):


    class Meta():
        fields = ['name', 'slug']
        model = Category


class GenreSerializer(serializers.ModelSerializer):


    class Meta():
        fields = ['name', 'slug']
        model = Genre


class TitleSerializer_post(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug', queryset=Genre.objects.all(), many=True)
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())

    class Meta():
        fields = '__all__'
        model = Title


class TitleSerializer_get(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta():
        fields = '__all__'
        model = Title

    def get_rating(self):
        #это заглушка, нужно дописать
        return 0
