from abc import ABC, abstractmethod
from src.build_index.processors.text_processor import TextProcessor

class BaseProcessor(ABC):
    
    PROCESSOR_MAPPING = {
        "txt": TextProcessor
    }

    @staticmethod
    def get_processor(extension: str):
        try:
            return PROCESSOR_MAPPING[extension]
        except _ as KeyError:
            raise Exception("Unsupported file extension provided.")

    @abstractmethod
    def tokenize(text: str):
        pass
