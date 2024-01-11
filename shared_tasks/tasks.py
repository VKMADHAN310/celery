from celery import shared_task
from .automation import AF

af=AF()

@shared_task(bind=True)
def autoo(self):
    af.msow()
    af.hca()
    af.babyf()
    af.mdquery()
    af.babyc()

# Define tasks for subtract, multiply, and divide similarly
