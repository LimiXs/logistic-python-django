import pdf2image
import pytesseract
import sys
import re
from pytesseract import Output
from trade_logistic.external_utils.miscellaneous import *


def get_doc_number(file_path):
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


# def print_docs_number(directory):
#     pdfs_paths = {}
#     try:
#         for file in os.listdir(directory):
#             if os.path.isfile(os.path.join(directory, file)):
#                 path = get_info_doc_numbers(os.path.join(directory, file))
#                 if path is None:
#                     shutil.move(os.path.join(directory, file), NOT_FOUND_PDFS_PATHS)
#                 pdfs_paths[file] = path
#     except FileNotFoundError:
#         print(f"Каталог {directory} не найден.")
#     except NotADirectoryError:
#         print(f"{directory} не является каталогом.")
#     except PermissionError:
#         print(f"Нет разрешения на чтение каталога {directory}.")
#
#     return pdfs_paths


# measure_execution_time(print_docs_number, PDFS_CATALOG)
# print(print_docs_number(PDFS_CATALOG_PATH))

# current_date = datetime.datetime.now()
# formatted_date = current_date.strftime('%d%m%Y')
#
# print(formatted_date)
