import os
import shutil


def count_files(catalog):
    return len([1 for x in list(os.scandir(catalog)) if x.is_file()])


def move_file(full_path, place):
    shutil.move(full_path, place)


# class FilesManager:
#     def __init__(self, directory):
#         self.directory = directory
#
#     def get_files_count(self):
#         return len([f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))])
#
#     def move_file(self, file_name, new_directory):
#         old_file_path = os.path.join(self.directory, file_name)
#         new_file_path = os.path.join(new_directory, file_name)
#         shutil.move(old_file_path, new_file_path)
