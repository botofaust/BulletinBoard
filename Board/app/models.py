from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    @staticmethod
    def standard_values():
        STANDARD_VALUES = ['Танки', 'Хилы', 'ДД', 'Торговцы', 'Гилдмастеры', 'Квестгиверы',
                           'Кузнецы', 'Кожевники', 'Зельевары', 'Мастера заклинаний']

        if not settings.DEBUG:
            return
        for value in STANDARD_VALUES:
            Category.objects.create(name=value)

    def __str__(self):
        return self.name


class Post(models.Model):
    POST_STATUS = [
        (0, 'Opened'),
        (-1, 'Closed'),
    ]

    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.IntegerField(choices=POST_STATUS, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'{self.created_on} {self.author} -> {self.post})'
