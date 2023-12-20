# from celery import shared_task
# from trade_logistic.external_utils.list_files import *
# from django.core.exceptions import ObjectDoesNotExist
#
# PDFS_CATALOG_PATH = r'D:\khomich\test'
#
#
# @shared_task
# def match_pdf_docs():
#     # from .models import DocumentInfo
#     pdf_dict = list_files(PDFS_CATALOG_PATH)
#     for num, path in pdf_dict.items():
#         print()
#         try:
#             print(True)
#             # record = DocumentInfo.objects.get(num_item=num)
#             # record.path_doc = path
#             # record.save()
#         except ObjectDoesNotExist:
#             print("Запись не найдена")
import random

from background_task import background


# import random
# from celery import shared_task
#
# @shared_task
@background
def my_task():
    return random.randint(1, 10)
