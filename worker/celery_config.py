from celery import Celery

app = Celery('celery_cal',broker='redis://localhost:6379/0')  # Redis broker URL
app.autodiscover_tasks(['shared_tasks'])
