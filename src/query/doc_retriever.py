import json
from collections import Counter, namedtuple

import numpy as np
from peewee import DoesNotExist
from sklearn.metrics.pairwise import cosine_similarity

from src.core.db.models import Document, Term
from src.index.processors.text_processor import TextProcessor
from src.schemas.search import DocumentRelevance, SearchRequest


class DocumentRetriever:
    def get_document_vector(self, posting_dict: dict, N: int, document_dimension: int) -> np.array:
        document_vector = np.zeros(document_dimension)

        max_f = max(posting_dict.values())

        for term_id, frequency in posting_dict.items():
            term_model = Term.get_by_id(term_id)
            tf_idf = (frequency / max_f) * (N / term_model.df)
            document_vector[int(term_id) - 1] = tf_idf

        return document_vector

    def __filter_documents(self, document_id_list: list[str], filters: dict):
        document_data = [Document.get(Document.document_id == document_id) for document_id in document_id_list]

        filtered_docs = list(
            filter(
                lambda doc: all(
                    (
                        not filters["extension"] or doc.file_extension == filters["extension"],
                        not filters["min_size"] or doc.size >= filters["min_size"],
                        not filters["max_size"] or doc.size <= filters["max_size"],
                        not filters["start_time"] or doc.modified >= filters["start_time"].replace(tzinfo=None),
                        not filters["end_time"] or doc.modified <= filters["end_time"].replace(tzinfo=None),
                        not filters["file_location"] or filters["file_location"] in doc.file_location,
                    )
                ),
                document_data,
            )
        )

        return [doc.document_id for doc in filtered_docs]

    def preprocess_query(self, query: str) -> list[str]:
        text_processor = TextProcessor()
        return text_processor.lemmatize(text_processor.tokenize(query))

    def retrieve_relevant_documents(self, query_data: SearchRequest) -> list[DocumentRelevance]:
        """
        :param: query_data: Contains all the query information. Schema same as Search Schema
        :return: the identifiers of the documents that contain any of the query terms
        """
        query_terms = self.preprocess_query(query_data.query)
        document_dimension = len(Term.select())
        N = len(Document.select())

        document_id_set = set()

        term_id_map = {}
        query_terms_exist = []

        for term in query_terms:
            try:
                term_model = Term.get(Term.term == term)
                query_terms_exist.append(term)
            except DoesNotExist as e:
                continue
            term_id_map[term] = term_model.term_id
            posting_docs = json.loads(term_model.doc_list)
            document_id_set = document_id_set.union(set(posting_docs))

        if len(query_terms_exist) == 0:
            return []

        query_counts = dict(Counter(query_terms_exist))

        retrieved_docs = self.__filter_documents(document_id_list=list(document_id_set), filters=query_data.dict())
        query_postings_dict = {term_id_map[term]: freq for term, freq in query_counts.items()}
        query_vector = self.get_document_vector(query_postings_dict, N, document_dimension)

        document_matrix = np.zeros((len(retrieved_docs), document_dimension))
        document_list: list[Document] = []

        for index, document_id in enumerate(retrieved_docs):
            document = Document.get_by_id(document_id)
            document_list.append(document)
            postings_dict = json.loads(document.postings)
            document_matrix[index] = self.get_document_vector(postings_dict, N, document_dimension)

        similarities = cosine_similarity(document_matrix, [query_vector]).flatten()

        doc_relevance_list = [
            DocumentRelevance(
                file_name=document.file_name,
                file_location=document.file_location,
                file_extension=document.file_extension,
                size=document.size,
                user=document.user,
                modified=document.modified,
                relevance=similarity,
            )
            for document, similarity in zip(document_list, similarities)
            if not document.deleted
        ]
        doc_relevance_list = sorted(doc_relevance_list, key=lambda x: x.relevance, reverse=True)

        return doc_relevance_list
