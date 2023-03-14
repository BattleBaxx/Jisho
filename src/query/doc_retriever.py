import json
from collections import Counter

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from src.core.db.models import Document, Term


class DocumentRetriever:
    def __init__(self):
        pass

    def get_document_vector(self, posting_dict: dict, N: int, document_dimension: int) -> np.array:
        document_vector = np.zeros(document_dimension)

        max_f = max(posting_dict.values())

        for term_id, frequency in posting_dict.items():
            term_model = Term.get_by_id(term_id)
            # print(frequency)
            # print(max_f)
            # print(N)
            # print(term_model.df)
            tf_idf = (frequency / max_f) * (N / term_model.df)
            # print(tf_idf)
            document_vector[int(term_id) - 1] = tf_idf

        # print(document_vector)
        return document_vector

    def retrieve_relevant_documents(self, query_terms: list[str]):
        """
        :param query_terms: a list of query term strings
        :return: the identifiers of the documents that contain any of the query terms
        """
        document_dimension = len(Term.select())
        N = len(Document.select())

        document_id_set = set()

        query_counts = dict(Counter(query_terms))
        term_id_map = {}

        for term in query_terms:
            term_model = Term.get(Term.term == term)
            term_id_map[term] = term_model.term_id
            posting_docs = json.loads(term_model.doc_list)
            document_id_set = document_id_set.union(set(posting_docs))

        query_postings_dict = {term_id_map[term]: freq for term, freq in query_counts.items()}
        query_vector = self.get_document_vector(query_postings_dict, N, document_dimension)

        document_matrix = np.zeros((len(document_id_set), document_dimension))

        for index, document_id in enumerate(document_id_set):
            document = Document.get_by_id(document_id)
            postings_dict = json.loads(document.postings)
            document_matrix[index] = self.get_document_vector(postings_dict, N, document_dimension)

        print(query_vector)
        print(document_matrix)

        print(cosine_similarity(document_matrix, [query_vector]))
