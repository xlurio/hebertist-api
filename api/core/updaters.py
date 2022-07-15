from apscheduler.schedulers.background import BackgroundScheduler
from core import models


def print_working_message():
    """Print a message if the scheduler is working"""
    print('Scheduler working...')


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(models.save_price_historic, 'interval', days=1)
    scheduler.start()
