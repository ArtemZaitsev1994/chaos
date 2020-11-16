from .common import *
import os


DEBUG = os.environ.get('DUBUG', True)

ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1']

BROKER_URL = os.environ.get('CELERY_BROKER', 'redis://localhost:6379')
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER', 'redis://localhost:6379')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_BACKEND = os.environ.get('CELERY_BACKEND', 'redis://localhost:6379')
CELERY_RESULT_SERIALIZER = 'json'
