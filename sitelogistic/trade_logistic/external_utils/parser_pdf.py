import pdf2image
import pytesseract
import sys
import os
import time
import re
import concurrent.futures
from pytesseract import Output

PDFS_CATALOG = r'\\10.137.2.200\doc$'
PDF_PATH = 'pdf_files/Scan20231114162725.pdf'
LANGUAGES = 'rus+eng'
DPI = 400
POPPLER_PATH = r'C:\Program Files\Poppler\Library\bin'
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
REQ_SYMBOLS = ('-', '/',)


def count_files(dir):
    return len([1 for x in list(os.scandir(dir)) if x.is_file()])


def measure_execution_time(func, *args):
    start_time = time.time()
    func(*args)
    end_time = time.time()
    print(f"Время выполнения функции: {end_time - start_time} секунд.")


def get_info_doc_numbers(file_path):
    try:
        images = pdf2image.convert_from_path(file_path, DPI, poppler_path=POPPLER_PATH)
    except FileNotFoundError:
        print(f'File {file_path} does not exist. Please check the file path and try again.')
        sys.exit()

    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
    number_pdf = ''
    for image in images:

        parsed_dict = pytesseract.image_to_data(image, lang=LANGUAGES, output_type=Output.DICT)

        if len(number_pdf) > 0:
            break

        number_pdf = ''
        text = ' '.join(parsed_dict['text'])
        text = re.sub(' +', ' ', text)

        for element in text.split(' '):
            if '-' in element and '/' in element and (len(element) == 24 or len(element) == 25):
                return element


def print_docs_number(directory):
    try:
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)):
                print(get_info_doc_numbers(os.path.join(directory, file)))
    except FileNotFoundError:
        print(f"Каталог {directory} не найден.")
    except NotADirectoryError:
        print(f"{directory} не является каталогом.")
    except PermissionError:
        print(f"Нет разрешения на чтение каталога {directory}.")


# measure_execution_time(print_docs_number, PDFS_CATALOG)
print(count_files(PDFS_CATALOG))
