from abc import ABC, abstractmethod


class BaseProcessor(ABC):

    @staticmethod
    def get_processor(extension: str):
        from src.build_index.processors.text_processor import TextProcessor

        PROCESSOR_MAPPING = {
            ".txt": TextProcessor
        }
        try:
            return PROCESSOR_MAPPING[extension]
        except _ as KeyError:
            raise KeyError("Unsupported file extension provided.")

    @abstractmethod
    def tokenize(text: str):
        pass
