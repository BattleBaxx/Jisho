import re
import nltk


class TextProcessor:
    lemmatizer = nltk.stem.WordNetLemmatizer()

    @staticmethod
    def tokenize(text: str):
        text = text.lower()
        text = re.sub("[^\w\s]", " ", text)
        text_tokens = nltk.word_tokenize(text)
        return [TextProcessor.lemmatizer.lemmatize(word) for word in text_tokens]
