from celery import Celery
import settings
import tasks

app = Celery("netadmin-worker")
app.config_from_object(settings)
app.autodiscover_tasks(["tasks"])
