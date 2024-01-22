from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
# from django.core.exceptions import ObjectDoesNotExist
from django_apscheduler.jobstores import DjangoJobStore
from trade_logistic.external_utils.file_manager import *

from .external_utils.parser_pdf import *
from .models import DocumentInfo
from .models import PDFDataBase

scheduler = None


def match_pdfs_docs():
    pdf_db_entries = PDFDataBase.objects.filter(in_use=False)

    count_in_db = pdf_db_entries.count()
    count_of_files = count_files(PDFS_CATALOG_PATH)
    print(count_in_db, count_of_files)

    directory = os.listdir(PDFS_CATALOG_PATH)
    for file in directory:
        file_path = os.path.join(PDFS_CATALOG_PATH, file)
        print(file_path)
        if not check_file_exists(DOWNLOAD_PDFS_PATHS, file):
            file_path = os.path.join(PDFS_CATALOG_PATH, file)
            move_file(file_path, DOWNLOAD_PDFS_PATHS)
    # if count_of_files == count_in_db:
    #     print(True)
    #     # for entry in pdf_db_entries:
    #     #     document_info_entry = DocumentInfo.objects.filter(num_item=entry.doc_number).first()
    #     #     if document_info_entry:
    #     #
    #     #         entry.in_use = True
    #     #         entry.save()
    #     #
    #     #         new_directory = PDFS_CATALOG_PATH + r'\download'
    #     #         new_full_path = os.path.join(new_directory, os.path.basename(entry.full_path))
    #     #         shutil.move(entry.full_path, new_full_path)
    #     #
    #     #         document_info_entry.path_doc = new_full_path
    #     #         document_info_entry.save()
    # else:
    #     pass
    #     directory = os.listdir(PDFS_CATALOG_PATH)
    #     for file in directory:
    #         file_path = os.path.join(PDFS_CATALOG_PATH, file)
    #         entry = PDFDataBase.objects.filter(full_path=file_path).first()
    #         if not entry:
    #             doc_number = get_doc_number(file_path)
    #             if doc_number is None:
    #                 move_file(file_path, NOT_FOUND_PDFS_PATHS)

                # entry = PDFDataBase(full_path=file_path, file_name=file)
                # entry.doc_number = get_doc_number(file_path)
                # entry.save()


def start_scheduler():
    global scheduler
    if scheduler is None:
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), 'default')
        scheduler.add_job(match_pdfs_docs, 'interval', minutes=2)
        scheduler.start()


start_scheduler()


# def my_task():
#     pdf_dict = list_files(PDFS_CATALOG_PATH)
#     for num, path in pdf_dict.items():
#         try:
#             record = DocumentInfo.objects.get(num_item=num)
#             record.path_doc = path
#             record.save()
#         except ObjectDoesNotExist:
#             print("Запись не найдена")
