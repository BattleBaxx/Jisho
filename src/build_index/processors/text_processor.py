import re

import nltk

from src.build_index.base_processor import BaseProcessor


class TextProcessor(BaseProcessor):
    lemmatizer = nltk.stem.WordNetLemmatizer()

    def tokenize(text: str):
        text = text.lower()
        text = re.sub("[^\w\s]", " ", text)
        text_tokens = nltk.word_tokenize(text)
        return [TextProcessor.lemmatizer.lemmatize(word) for word in text_tokens]
