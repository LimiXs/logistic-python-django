from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from trade_logistic.external_utils.file_manager import *
from .external_utils.connecter_fdb import get_data_fdb, HOSTNAME, DATABASE_PATH, USERNAME, PASSWORD

from .external_utils.parser_pdf import *
from .models import DocumentInfo
from .models import PDFDataBase

scheduler = None


def match_pdfs_docs():
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
                download_path = os.path.join(CATALOG_DOWNLOAD_PDFS, file)
                try:
                    record = PDFDataBase(doc_number=doc_number, full_path=download_path, file_name=file)
                    record.save()
                except Exception as e:
                    print(f"Ошибка при сохранении записи: {e}")

            new_file_path = os.path.join(new_directory, file)
            if os.path.exists(new_file_path):
                os.remove(new_file_path)
            shutil.move(file_path, new_directory)

    pdf_data = PDFDataBase.objects.all()
    for pdf in pdf_data:
        doc_info = DocumentInfo.objects.filter(num_item=pdf.doc_number)
        if doc_info.exists():
            doc_info.update(path_doc=pdf.full_path)

            pdf.in_use = True
            pdf.save()


def upload_docs_db():
    records = get_data_fdb(HOSTNAME, DATABASE_PATH, USERNAME, PASSWORD)
    for record in records:
        if not DocumentInfo.objects.filter(num_item=record[0]).exists():
            DocumentInfo.objects.create(
                date_placement=record[1],
                num_item=record[0],
                num_transport=record[3].replace(';', '; '),
                num_doc=record[4],
                date_docs=record[7],
                documents=record[6],
                status=record[9],
                num_nine=record[10],
                num_td=record[11] if record[11] is None else record[11][:30].replace(';', '; ')
            )


def start_scheduler():
    global scheduler
    if scheduler is None:
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), 'default')
        scheduler.add_job(upload_docs_db, 'interval', minutes=30)
        scheduler.add_job(match_pdfs_docs, 'interval', minutes=5)
        scheduler.start()


start_scheduler()
