from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    subscribers = models.ManyToManyField(User)

    def subscribe(self, user):
        self.subscribers.add(user)

    def unsubscribe(self, user):
        self.subscribers.remove(user)

    @property
    def get_subscribers_id(self):
        return self.subscribers.all().values_list('pk', flat=True)

    @staticmethod
    def populate_standard_values():
        """
        Оставим это тут для первичного заполнения категорий
        """
        STANDARD_VALUES = ['Танки', 'Хилы', 'ДД', 'Торговцы', 'Гилдмастеры', 'Квестгиверы',
                           'Кузнецы', 'Кожевники', 'Зельевары', 'Мастера заклинаний']

        if not settings.DEBUG:
            return
        for value in STANDARD_VALUES:
            Category.objects.create(name=value)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    content обычное текстовое поле, заполняется с помощью редактора summernote, в шаблонах потребуется autoescape off
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'{self.created_on} {self.author} -> {self.post})'

    def sent_email_about_create(self):
        """
        посылаем письмо автору поста, вызывается сигналом post_save
        """
        url = 'http://127.0.0.1:8000' + reverse('post_detail', kwargs={'pk': self.post.id})
        subject, from_email, to = 'Новый комментарий', settings.SERVER_EMAIL, self.post.author.email
        text_content = 'Получен новый комментарий'
        html_content = f'<p>Добавлен новый комментарий<br><br><a href={url}>Посмотреть на сайте</a></p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def sent_email_about_accept(self):
        """
        посылаем письмо автору коммента, вызывается из вьюшки accept_comment
        """
        url = 'http://127.0.0.1:8000' + reverse('post_detail', kwargs={'pk': self.post.id})
        subject, from_email, to = 'Ваше предложение приняли', settings.SERVER_EMAIL, self.author.email
        text_content = 'Ваше предложение приняли'
        html_content = f'<p>Ваше предложение приняли<br><br><a href={url}>Посмотреть на сайте</a></p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
