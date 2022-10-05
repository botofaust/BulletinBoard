import datetime

from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Comment, Post, Category


@shared_task
def sent_email_about_create(comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        pass
    else:
        comment.sent_email_about_create()


@shared_task
def sent_email_about_accept(comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        pass
    else:
        comment.sent_email_about_accept()


def sent_email_to_subscriber(user, posts_list):
    html_content = render_to_string(
        'app/post_email.html',
        {
            'posts': posts_list,
            'user': user,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Новые публикации за неделю',
        body='Новые публикации за неделю',
        from_email=settings.SERVER_EMAIL,
        to=[user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def weekly_mailing():
    date = timezone.now() - datetime.timedelta(days=7)
    for user in User.objects.all():
        posts = Post.objects.filter(created_on__gte=date, category__subscribers=user.pk)
        if posts:
            sent_email_to_subscriber(user, posts)
