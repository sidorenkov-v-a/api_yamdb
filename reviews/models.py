from django.db import models
from titles.models import Title
from django.core.validators import MinValueValidator, MaxValueValidator

# Forgot this
from django.contrib.auth import get_user_model
User = get_user_model()


class Review(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews', verbose_name='Произведение')
    # Wtf :) ???
    # author = author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='Автор')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='Автор')

    text = models.TextField('Комментарий оценки')
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField('Дата и время', auto_now_add=True)

    def __str__(self):
        self.pk

    class Meta:
        ordering = ['-pub_date']


class Comment(models.Model):
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments', verbose_name='Оценка')
    author = author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    text = models.TextField('Комментарий к оценке')
    pub_date = models.DateTimeField('Дата и время', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
