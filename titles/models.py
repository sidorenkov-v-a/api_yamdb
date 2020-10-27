from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=30)


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=30)


class Title(models.Model):
    name = models.TextField(max_length=100)
    year = models.IntegerField()
    description = models.TextField(max_length=400)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='titles'
        )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='titles'
        )
