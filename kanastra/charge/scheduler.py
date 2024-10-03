import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from charge.emails_tasks import send_emails
from atexit import register


def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        send_emails,
        trigger=IntervalTrigger(minutes=1),
        id="scheduled_emails",
        replace_existing=True,
    )

    scheduler.start()

    register(lambda: scheduler.shutdown())
