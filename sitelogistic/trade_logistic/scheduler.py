from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from django.core.exceptions import ObjectDoesNotExist
from django_apscheduler.jobstores import DjangoJobStore
from sitelogistic.settings import PDFS_CATALOG_PATH
from trade_logistic.external_utils.list_files import *
from trade_logistic.external_utils.file_manager import *
from .models import DocumentInfo
from .models import PDFDataBase


def match_pdfs_docs():
    pdf_db_entries = PDFDataBase.objects.filter(in_use=False)
    count_in_db = pdf_db_entries.count()
    count_of_files = count_files(PDFS_CATALOG_PATH)

    if count_of_files == count_in_db:
        # чекать из бд, если нашли то менять статус
        for entry in pdf_db_entries:
            document_info_entry = DocumentInfo.objects.filter(num_item=entry.doc_number).first()
            if document_info_entry:

                entry.in_use = True
                entry.save()

                new_directory = '/path/to/new/directory'  # Замените на путь к новому каталогу
                new_path = os.path.join(new_directory, os.path.basename(entry.full_path))
                shutil.move(entry.full_path, new_path)

                document_info_entry.path_doc = entry.full_path
                document_info_entry.save()
    else:
        # парсить новый файл и записывать в бд
        pass


def my_task():
    pdf_dict = list_files(PDFS_CATALOG_PATH)
    for num, path in pdf_dict.items():
        try:
            record = DocumentInfo.objects.get(num_item=num)
            record.path_doc = path
            record.save()
        except ObjectDoesNotExist:
            print("Запись не найдена")


def do_main_task():
    pass


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')
    scheduler.add_job(my_task, 'interval', minutes=60)
    scheduler.start()

# start_scheduler()
