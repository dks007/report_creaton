"""
Celery Basic configuration
"""

# python imports
import os

# third party imports
from celery import Celery
from django.conf import settings
from dotenv import load_dotenv

# OR, the same with increased verbosity:
load_dotenv(verbose=True)

env_path = os.path.join(os.path.abspath(os.path.join('.env', os.pardir)), '.env')

load_dotenv(dotenv_path=env_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('SETTINGS'))

app = Celery()

app.config_from_object('django.conf:settings')

# Load task modules from all registered Django apps.
app.autodiscover_tasks(settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    """ celery debug task """
    print(f'Request: {self.request!r}')
