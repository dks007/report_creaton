# success_tool/celery.py
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'success_tool.settings')

# create a Celery instance and configure it with the Django settings.
app = Celery('success_tool')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Celery Beat schedule
app.conf.beat_schedule = {
    'fetch-and-save-jira-data': {
        'task': 'success_tool.tasks.fetch_and_save_jira_data',
        'schedule': crontab(minute=0, hour=0),  # Adjust the schedule as needed
    },
}
