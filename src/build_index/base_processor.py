import re
from abc import ABC, abstractmethod

import nltk


class BaseProcessor(ABC):
    lemmatizer = nltk.stem.WordNetLemmatizer()

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
