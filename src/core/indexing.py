import json
import os
from collections import Counter

from src.build_index.base_processor import BaseProcessor
from src.build_index.processor_factory import ProcessorFactory
from src.core.db.models import Document, Term


def __update_doc_lists(term_id_doc_set_map: dict):
    for term_id, doc_set in term_id_doc_set_map.items():
        term_model: Term = Term.get_by_id(term_id)
        existing_doc_set = set(json.loads(term_model.doc_list))
        updated_doc_set = existing_doc_set.union(doc_set)
        term_model.df = len(updated_doc_set)
        term_model.doc_list = json.dumps(list(updated_doc_set))

        term_model.save()


def __get_file_terms(file_details: list[tuple[str, str]]) -> list[list[str]]:
    file_terms = list()
    for file_path, file_extension in file_details:
        processor = ProcessorFactory.get_processor(file_extension)
        file_terms.append(processor.preprocessed_tokens(file_path=file_path))
    return file_terms


def __get_file_location(file_path: str) -> tuple[str, str, str]:
    file_pref, file_extension = os.path.splitext(file_path)
    file_location = os.path.dirname(file_pref)
    file_name = os.path.basename(file_pref)
    return file_location, file_name, file_extension


def handle_create(file_paths: list[str]):
    file_details = list(map(lambda path: (path, __get_file_location(path)[2]), file_paths))

    file_terms = __get_file_terms(file_details)

    vocabulary = set(term for term_list in file_terms for term in term_list)

    # Key: term Value: term_id
    term_id_map = {}
    for term in vocabulary:
        term, created = Term.get_or_create(term=term)
        term_id_map[term.term] = term.term_id

    # Key: Index of document in file_paths Value: document_id
    doc_index_id_map = {}

    for doc_index, file_path in enumerate(file_paths):
        file_location, file_name, file_extension = __get_file_location(file_path)
        doc_terms = file_terms[doc_index]
        term_freq_dict = {term_id_map[term]: freq for term, freq in dict(Counter(doc_terms)).items()}
        doc = Document.create(
            file_name=file_name,
            file_location=file_location,
            postings=json.dumps(term_freq_dict),
            file_extension=file_extension,
        )
        doc_index_id_map[doc_index] = doc.document_id

    term_id_doc_set_map = {}
    for doc_index, doc_terms in enumerate(file_terms):
        terms = set(doc_terms)

        for term in terms:
            term_id = term_id_map[term]
            term_set = term_id_doc_set_map.setdefault(term_id, set())
            term_set.add(doc_index_id_map[doc_index])

    __update_doc_lists(term_id_doc_set_map)
