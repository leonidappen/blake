import click
from flask.cli import with_appcontext
from celery.bin import worker as celery_worker
from celery.bin import beat as celery_beat

from app.extensions import celery as celery_obj


@click.group()
def celery():
    """Celery misc"""
    pass

@celery.command()
def beat():
    beat = celery_beat.beat(app=celery_obj)
    beat.run()

@celery.command()
@with_appcontext
def worker():
    worker = celery_worker.worker(app=celery_obj)
    worker.run()