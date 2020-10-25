from rest_framework import serializers

from titles.models import Title, Category, Genre


class CategorySerializer(serializers.ModelSerializer):


    class Meta():
        fields = ['name', 'slug']
        model = Category


class GenreSerializer(serializers.ModelSerializer):


    class Meta():
        fields = ['name', 'slug']
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta():
        fields = '__all__'
        model = Title

    def get_rating(self):
        #это заглушка, нужно дописать
        return 0
