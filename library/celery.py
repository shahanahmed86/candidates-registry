from celery import Celery

from configs import configs

celery_client = Celery(__name__, broker=configs.BROKER, backend=configs.BROKER)
