from celery import Celery

from config import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


class Config:
    CELERY_RESULT_BACKEND = 'redis'
    BROKER_URL = 'redis://localhost:6379/0'
    CELERY_IMPORTS = ('submission.tasks',)


app = Celery('judge')
app.config_from_object(Config)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
