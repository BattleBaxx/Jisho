from src.build_index.base_processor import BaseProcessor


class TextProcessor(BaseProcessor):
    def parse_doc(self, file_path: str) -> str:
        return open(file_path).read(-1)
