import re

import nltk
from docx2txt import docx2txt

from src.build_index.base_processor import BaseProcessor


class DocxProcessor(BaseProcessor):
    lemmatizer = nltk.stem.WordNetLemmatizer()

    def tokenize(file_path: str):
        file_content = docx2txt.process(file_path)
        file_content = file_content.lower()
        file_content = re.sub("[^\w\s]", " ", file_content)
        text_tokens = nltk.word_tokenize(file_content)
        return [DocxProcessor.lemmatizer.lemmatize(word) for word in text_tokens]
