import sys
import os
import re
import shutil


def count_files(catalog):
    return len([1 for x in list(os.scandir(catalog)) if x.is_file()])


# def move_file(directory prefix=''):
#     shutil.move(os.path.join(directory, file), NOT_FOUND_PDFS_PATHS)


class FilesManager:
    def __init__(self, directory):
        self.directory = directory

    def get_files_count(self):
        return len([f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))])

    def move_file(self, file_name, new_directory):
        old_file_path = os.path.join(self.directory, file_name)
        new_file_path = os.path.join(new_directory, file_name)
        shutil.move(old_file_path, new_file_path)

    # def get_file_size(self, file_name):
    #     file_path = os.path.join(self.directory, file_name)
    #     return os.path.getsize(file_path)


PDFS_CATALOG_PATH = r'\\10.137.2.200\doc$'
print(count_files(PDFS_CATALOG_PATH))
