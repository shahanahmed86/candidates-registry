from celery import Celery

from configs import configs

app = Celery(__name__, broker=configs.BROKER, backend=configs.BROKER)

@app.task
def add(x, y):
    return x + y
