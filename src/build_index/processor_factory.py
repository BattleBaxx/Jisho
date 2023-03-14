from src.build_index.processors.docx_processor import DocxProcessor
from src.build_index.processors.image_processor import ImageProcessor
from src.build_index.processors.pdf_processor import PdfProcessor
from src.build_index.processors.text_processor import TextProcessor

PROCESSOR_MAPPING = {
    ".txt": TextProcessor,
    ".docx": DocxProcessor,
    ".png": ImageProcessor,
    ".jpeg": ImageProcessor,
    ".ppm": ImageProcessor,
    ".tiff": ImageProcessor,
    ".bmp": ImageProcessor,
    ".pdf": PdfProcessor,
}

SINGLETON_MAPPING = {}


class ProcessorFactory:
    @staticmethod
    def get_processor(extension: str):
        try:
            extension_class = PROCESSOR_MAPPING[extension]
            if extension_class not in SINGLETON_MAPPING:
                SINGLETON_MAPPING[extension_class] = extension_class()

            return SINGLETON_MAPPING[extension_class]
        except KeyError:
            raise KeyError("Unsupported file extension provided.")
