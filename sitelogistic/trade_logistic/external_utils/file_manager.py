import sys
import os
import re
import shutil


class FilesManager:
    def __init__(self, catalog):
        self.catalog = catalog

    def count_files(self):
        return len([1 for x in list(os.scandir(self.catalog)) if x.is_file()])
