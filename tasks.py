from __future__ import absolute_import

import os

from celery import Celery

app = Celery('example_celery',
             broker=os.environ.get('CELERY_BROKER_URL', 'amqp://guest@localhost//'),
             backend=os.environ.get('CELERY_RESULT_BACKEND', 'amqp://guest@localhost//'),
             include=['tasks'])


@app.task(bind=True)
def example_task(self, a, b):
    return a + b