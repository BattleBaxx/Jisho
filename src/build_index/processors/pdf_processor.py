from PyPDF2 import PdfReader

from src.build_index.base_processor import BaseProcessor


class PdfProcessor(BaseProcessor):
    def parse_doc(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        return " ".join([page.extract_text() for page in reader.pages])
