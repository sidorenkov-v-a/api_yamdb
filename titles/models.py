from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='название категории')
    slug = models.SlugField(unique=True, max_length=30)


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='название жанра')
    slug = models.SlugField(unique=True, max_length=30)


class Title(models.Model):
    name = models.CharField(max_length=100, verbose_name='название тайтла')
    year = models.PositiveSmallIntegerField('год выпуска')
    description = models.TextField(max_length=400, verbose_name='описание')
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
        verbose_name='жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='категория'
    )

    class Meta:
        ordering = ['-year']
