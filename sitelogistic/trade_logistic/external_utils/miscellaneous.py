# pdf-documents paths
BASE_CATALOG = r'\\10.137.2.200\doc$'
PDFS_CATALOG_PATH = BASE_CATALOG + r'\parsing_pdfs'
NOT_FOUND_PDFS_PATHS = PDFS_CATALOG_PATH + r'\not_found_doc_pdfs'
DOWNLOAD_PDFS_PATHS = PDFS_CATALOG_PATH + r'\download\\'

# settings for parsing pdfs
LANGUAGES = 'rus+eng'
DPI = 400
POPPLER_PATH = r'C:\Program Files\Poppler\Library\bin'
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
REQ_SYMBOLS = ('-', '/',)
