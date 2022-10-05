import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Board.settings')

celery_app = Celery('app')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.conf.beat_schedule = {
    'mailing_every_monday_8am': {
        'task': 'app.tasks.weekly_mailing',
        'schedule': crontab(minute=0, hour=8, day_of_week=1),
    },
}
celery_app.autodiscover_tasks()


