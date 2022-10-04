from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post, Comment


@receiver(post_save, sender=Comment)
def comment_callback(sender, **kwargs):
    kwargs['instance'].send_email()
