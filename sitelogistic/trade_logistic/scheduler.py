from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
# from django.core.exceptions import ObjectDoesNotExist
from django_apscheduler.jobstores import DjangoJobStore
from django.db import IntegrityError
from django.db.models import F
from trade_logistic.external_utils.file_manager import *

from .external_utils.parser_pdf import *
from .models import DocumentInfo
from .models import PDFDataBase

scheduler = None


def match_pdfs_docs():
    # pdf_db_entries = PDFDataBase.objects.filter(in_use=False)
    # count_in_db = pdf_db_entries.count()
    count_of_files = count_files(CATALOG_PDFS)

    directory = os.listdir(CATALOG_PDFS)
    if count_of_files > 0:
        for file in directory:
            extension = os.path.splitext(file)[1]
            file_path = os.path.join(CATALOG_PDFS, file)

            doc_number = get_doc_number(file_path) if extension == PDF else None
            if doc_number is None or extension != PDF:
                new_directory = CATALOG_NOT_FOUND_FILES
            else:
                new_directory = CATALOG_DOWNLOAD_PDFS
                full_path = os.path.join(CATALOG_DOWNLOAD_PDFS, file)
                try:
                    record = PDFDataBase(doc_number=doc_number, full_path=full_path, file_name=file)
                    record.save()
                except IntegrityError:
                    print('Not saved')
            move_file(file_path, new_directory)

    pdf_data = PDFDataBase.objects.all()
    for pdf in pdf_data:
        doc_info = DocumentInfo.objects.filter(num_item=pdf.doc_number)
        if doc_info.exists():
            doc_info.update(path_doc=F('full_path'))

            pdf.in_use = True
            pdf.save()


def start_scheduler():
    global scheduler
    if scheduler is None:
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), 'default')
        scheduler.add_job(match_pdfs_docs, 'interval', minutes=5)
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

# for file in directory:
    #     file_path = os.path.join(CATALOG_PDFS, file)
    #     print(file_path)
    #     if not check_file_exists(CATALOG_DOWNLOAD_PDFS, file):
    #         file_path = os.path.join(CATALOG_PDFS, file)
    #         move_file(file_path, CATALOG_DOWNLOAD_PDFS)


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