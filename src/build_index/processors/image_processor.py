import pytesseract
from PIL import Image

from src.build_index.base_processor import BaseProcessor


class ImageProcessor(BaseProcessor):
    def parse_doc(self, file_path: str) -> str:
        image = Image.open(file_path)
        config = r"--oem 1"
        return pytesseract.image_to_string(image, config=config)
