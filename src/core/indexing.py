from __future__ import annotations

import json
import os
from collections import Counter

from src.core.db.models import Document, Term
from src.core.util import get_file_metadata
from src.index.processor_factory import ProcessorFactory


class Indexer:
    indexer = None

    @staticmethod
    def get_instance() -> Indexer:
        if not Indexer.indexer:
            Indexer.indexer = Indexer()

        return Indexer.indexer

    def update_doc_lists(self, term_id: str, doc_set: set) -> None:
        term_model: Term = Term.get_by_id(term_id)
        existing_doc_set = set(json.loads(term_model.doc_list))
        updated_doc_set = existing_doc_set.union(doc_set)
        term_model.df = len(updated_doc_set)
        term_model.doc_list = json.dumps(list(updated_doc_set))

        term_model.save()

    @staticmethod
    def __get_file_terms(file_details: list[tuple[str, str]]) -> list[list[str]]:
        file_terms = list()
        for file_path, file_extension in file_details:
            processor = ProcessorFactory.get_processor(file_extension)
            file_terms.append(processor.preprocessed_tokens(file_path=file_path))
        return file_terms

    @staticmethod
    def __get_file_location(file_path: str) -> tuple[str, str, str]:
        file_pref, file_extension = os.path.splitext(file_path)
        file_location = os.path.dirname(file_pref)
        file_name = os.path.basename(file_pref)
        return file_location, file_name, file_extension

    def index_files(self, file_paths: list[str]):
        file_details = list(map(lambda path: (path, self.__get_file_location(path)[2]), file_paths))

        file_terms = self.__get_file_terms(file_details)

        vocabulary = set(term for term_list in file_terms for term in term_list)

        # Key: term Value: term_id
        term_id_map = {}
        for term in vocabulary:
            term, created = Term.get_or_create(term=term)
            term_id_map[term.term] = term.term_id

        # Key: Index of document in file_paths Value: document_id
        doc_index_id_map = {}

        for doc_index, file_path in enumerate(file_paths):
            file_location, file_name, file_extension = self.__get_file_location(file_path)
            doc_terms = file_terms[doc_index]
            term_freq_dict = {term_id_map[term]: freq for term, freq in dict(Counter(doc_terms)).items()}
            doc, _ = Document.get_or_create(
                file_name=file_name, file_location=file_location, file_extension=file_extension, deleted=False
            )
            doc.postings = json.dumps(term_freq_dict)
            doc.user, doc.size, doc.modified = get_file_metadata(file_path)
            doc.save()

            doc_index_id_map[doc_index] = doc.document_id

        term_id_doc_set_map = {}
        for doc_index, doc_terms in enumerate(file_terms):
            terms = set(doc_terms)

            for term in terms:
                term_id = term_id_map[term]
                term_set = term_id_doc_set_map.setdefault(term_id, set())
                term_set.add(doc_index_id_map[doc_index])

        for term_id, doc_set in term_id_doc_set_map.items():
            self.update_doc_lists(term_id, doc_set)

    def mark_deleted(self, file_paths: list[str]):
        file_path_set = set(file_paths)
        print(file_path_set)

        all_indexed_documents = list(Document.select())
        for doc in all_indexed_documents:
            doc_full_file_path = os.path.join(doc.file_location, (doc.file_name + doc.file_extension))
            if doc_full_file_path not in file_path_set:
                doc.deleted = True
                doc.save()
