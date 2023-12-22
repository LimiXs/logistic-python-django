from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # Здесь добавьте ваши задачи...
    print(True)
    # Конец
    scheduler.start()
