import os


from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chaos.settings.dev')

app = Celery('chaos')
app.config_from_object('django.conf:settings')
app.conf.beat_schedule = {

}
app.autodiscover_tasks()
