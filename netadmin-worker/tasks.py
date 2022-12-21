from celery import shared_task
from maxmind import MaxMind

@shared_task(name="worker.tasks.broad_message")
def broad_message(message, *args, **kwargs):
    print(message["router"])
    return True
