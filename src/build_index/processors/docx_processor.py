from docx2txt import docx2txt

from src.build_index.base_processor import BaseProcessor


class DocxProcessor(BaseProcessor):
    def parse_doc(self, file_path: str) -> str:
        return docx2txt.process(file_path)
