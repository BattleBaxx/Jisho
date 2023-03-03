import re

import nltk

from src.build_index.base_processor import BaseProcessor


class TextProcessor(BaseProcessor):
    lemmatizer = nltk.stem.WordNetLemmatizer()

    def tokenize(file_path: str):
        text = open(file_path).read(-1),
        text = text[0].lower()
        text = re.sub("[^\w\s]", " ", text)
        text_tokens = nltk.word_tokenize(text)
        return [TextProcessor.lemmatizer.lemmatize(word) for word in text_tokens]
