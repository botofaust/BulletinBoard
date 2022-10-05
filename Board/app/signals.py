from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Comment
from .tasks import sent_email_about_create


@receiver(post_save, sender=Comment)
def comment_callback(sender, **kwargs):
    instance = kwargs['instance']
    if kwargs['created']:
        sent_email_about_create.delay(instance.pk)
