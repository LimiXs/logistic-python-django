import sys
import os
import re
import shutil


def count_files(catalog):
    return len([1 for x in list(os.scandir(catalog)) if x.is_file()])


# class FilesManager:
#     def __init__(self, catalog):
#         self.catalog = catalog
#
#     def count_files(self):
#         return len([1 for x in list(os.scandir(self.catalog)) if x.is_file()])

PDFS_CATALOG_PATH = r'\\10.137.2.200\doc$'
print(count_files(PDFS_CATALOG_PATH))
