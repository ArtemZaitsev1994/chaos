from .common import *


DEBUG = os.environ.get('DEBUG', False)

ALLOWED_HOSTS = ['0.0.0.0', 'chaos', 'localhost', '127.0.0.1', '185.10.184.226']

CORS_ALLOWED_ORIGINS = [
    "http://0.0.0.0",
    "http://localhost",

    "http://127.0.0.1",
    "http://185.10.184.226",
    "http://185.10.184.226:1337",

    "http://127.0.0.1:3001",
    "http://0.0.0.0:3001",
    "http://localhost:3001",
    "http://185.10.184.226:3001",

]

BROKER_URL = os.environ.get('CELERY_BROKER', 'redis://redis:6379')
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER', 'redis://redis:6379')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_BACKEND = os.environ.get('CELERY_BACKEND', 'redis://redis:6379')
CELERY_RESULT_SERIALIZER = 'json'

