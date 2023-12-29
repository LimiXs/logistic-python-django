from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from django.core.exceptions import ObjectDoesNotExist
from django_apscheduler.jobstores import DjangoJobStore
from sitelogistic.settings import PDFS_CATALOG_PATH
from trade_logistic.external_utils.list_files import *
from .models import DocumentInfo


def my_task():
    pdf_dict = list_files(PDFS_CATALOG_PATH)
    for num, path in pdf_dict.items():
        try:
            record = DocumentInfo.objects.get(num_item=num)
            record.path_doc = path
            record.save()
        except ObjectDoesNotExist:
            print("Запись не найдена")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')
    scheduler.add_job(my_task, 'interval', minutes=60)
    scheduler.start()


# start_scheduler()
