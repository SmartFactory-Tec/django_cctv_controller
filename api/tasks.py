from celery import shared_task
from cctv_controller.celery import app
from celery.utils.log import get_task_logger
from datetime import datetime


logger = get_task_logger(__name__)


@shared_task
def repeated_function():
    # Your repeated function logic goes here
    logger.info("Adding 111")
    print("Running the function repeatedly")

    now = datetime.now()  # current date and time

    return True


@app.on_after_configure.connect
def add_periodic(**kwargs):
    app.add_periodic_task(1.0, repeated_function.s(), name="add every 10")
