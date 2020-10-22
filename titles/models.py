from django.db import models


# class Catigory(models.Model):
class Category(models.Model):
    name = models.CharField(max_length=100)
    # What unicode is???
    # slug = models.SlugField(unicode=True, max_length=30)
    slug = models.SlugField(max_length=30)


class Genre(models.Model):
    name = models.CharField(max_length=100)
    # What unicode is???
    # slug = models.SlugField(unicode=True, max_length=30)
    slug = models.SlugField(max_length=30)


class Title(models.Model):
    name = models.CharField(max_length=100)
    year = models.DateField()
    description = models.TextField(max_length=400)
    # Where is rating field???
    # rating =

    # Where is on_delete field???
    # genre = models.ForeignKey('Generes')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    # Where is on_delete field???
    # category = models.ForeignKey('Categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

