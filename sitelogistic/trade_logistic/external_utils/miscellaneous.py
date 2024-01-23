# pdf-documents paths
BASE_CATALOG = r'\\10.137.2.200\doc$'
CATALOG_PDFS = BASE_CATALOG + r'\parsing_pdfs'
CATALOG_NOT_FOUND_FILES = BASE_CATALOG + r'\not_found_doc_files'
CATALOG_DOWNLOAD_PDFS = BASE_CATALOG + r'\download_pdfs'
PDF = '.pdf'

# settings for parsing pdfs
LANGUAGES = 'rus+eng'
DPI = 400
POPPLER_PATH = r'C:\Program Files\Poppler\Library\bin'
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
REQ_SYMBOLS = ('-', '/',)
