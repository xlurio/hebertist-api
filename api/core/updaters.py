from apscheduler.schedulers.background import BackgroundScheduler
# noinspection PyUnresolvedReferences
from core import models


def print_working_message():
    """Print a message if the scheduler is working"""
    print('Scheduler working...')


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(models.update_game_model, 'interval', days=30)
    scheduler.add_job(models.update_price_model, 'interval', days=7)
    scheduler.add_job(models.save_price_historic, 'interval', days=10)
    scheduler.start()
