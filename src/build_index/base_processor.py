from abc import ABC, abstractmethod
import re

import nltk



class BaseProcessor(ABC):
    lemmatizer = nltk.stem.WordNetLemmatizer()

    @staticmethod
    def get_processor(extension: str):
        from src.build_index.processors.text_processor import TextProcessor
        from src.build_index.processors.docx_processor import DocxProcessor
        from src.build_index.processors.image_processor import ImageProcessor
        from src.build_index.processors.pdf_processor import PdfProcessor

        PROCESSOR_MAPPING = {
            ".txt": TextProcessor(),
            ".docx": DocxProcessor(),
            ".png": ImageProcessor(),
            ".jpeg": ImageProcessor(),
            ".ppm": ImageProcessor(),
            ".tiff": ImageProcessor(),
            ".bmp": ImageProcessor(),
            ".pdf": PdfProcessor()
        }
        try:
            return PROCESSOR_MAPPING[extension]
        except KeyError:
            raise KeyError("Unsupported file extension provided.")

    def preprocessed_tokens(self, file_path: str):
        doc_contents = self.parse_doc(file_path)
        tokens = self.tokenize(doc_contents)
        lemmatized_tokens = self.lemmatize(tokens)
        return lemmatized_tokens

    @abstractmethod
    def parse_doc(self, file_path: str) -> str:
        pass

    def tokenize(self, content: str) -> list[str]:
        content = content.lower()
        content = re.sub("[^\w\s]", " ", content)
        return nltk.word_tokenize(content)

    def lemmatize(self, tokens: list[str]) -> list[str]:
        return [BaseProcessor.lemmatizer.lemmatize(word) for word in tokens]
