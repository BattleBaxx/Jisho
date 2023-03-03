from abc import ABC, abstractmethod


class BaseProcessor(ABC):

    @staticmethod
    def get_processor(extension: str):
        from src.build_index.processors.text_processor import TextProcessor
        from src.build_index.processors.docx_processor import DocxProcessor

        PROCESSOR_MAPPING = {
            ".txt": TextProcessor,
            ".docx": DocxProcessor
        }
        try:
            return PROCESSOR_MAPPING[extension]
        except _ as KeyError:
            raise KeyError("Unsupported file extension provided.")

    @abstractmethod
    def tokenize(self, text: str):
        pass
