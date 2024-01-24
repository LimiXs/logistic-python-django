import os
import shutil


def count_files(catalog):
    return len([1 for x in list(os.scandir(catalog)) if x.is_file()])


def move_file(full_path, new_directory):

    shutil.move(full_path, new_directory)


def file_exists(directory, filename):
    file_path = os.path.join(directory, filename)
    return os.path.isfile(file_path)


class FileManager:
    def __init__(self, directory: str):
        self.directory = directory

    def count_files(self) -> int:
        return len([1 for x in list(os.scandir(self.directory)) if x.is_file()])

    def move_file(self, filename: str, new_directory: str):
        full_path = os.path.join(self.directory, filename)
        if os.path.isfile(full_path):
            shutil.move(full_path, new_directory)
        else:
            print(f"Файл {filename} не найден в {self.directory}")

    def check_file_exists(self, filename: str) -> bool:
        file_path = os.path.join(self.directory, filename)
        return os.path.isfile(file_path)
