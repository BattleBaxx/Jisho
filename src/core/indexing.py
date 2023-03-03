import os
import json

from src.build_index.base_processor import BaseProcessor
from src.core.db.models import Term, Document
from collections import Counter


def __update_postings(term_id_postings_map: dict):
    for term_id, posting_map in term_id_postings_map.items():
        term_model: Term = Term.get_by_id(term_id)
        existing_posting_string = term_model.posting_list
        existing_posting_dict = json.loads(existing_posting_string)

        updated_posting_dict = {**existing_posting_dict, **posting_map}
        updated_posting_string = json.dumps(updated_posting_dict)
        term_model.posting_list = updated_posting_string
        term_model.df = len(updated_posting_dict.keys())

        term_model.save()


def __get_file_terms(file_details: list[tuple[str, str]]) -> list[list[str]]:
    file_terms = list()
    for file_path, file_extension in file_details:
        processor = BaseProcessor.get_processor(file_extension)
        file_terms.append(processor.tokenize(file_path))
    return file_terms


def __get_file_metadata(file_path: str) -> tuple[str, str, str]:
    file_pref, file_extension = os.path.splitext(file_path)
    file_location = os.path.dirname(file_pref)
    file_name = os.path.basename(file_pref)
    return file_location, file_name, file_extension


def handle_create(file_paths: list[str]):
    file_details = list(map(lambda path: (path, __get_file_metadata(path)[2]), file_paths))

    file_terms = __get_file_terms(file_details)

    vocabulary = set(term for term_list in file_terms for term in term_list)

    term_id_map = {}
    for term in vocabulary:
        term_id, created = Term.get_or_create(term=term)
        term_id_map[term] = term_id

    doc_index_id_map = {}

    for doc_index, file_path in enumerate(file_paths):
        file_pref, file_extension = os.path.splitext(file_path)
        file_location = os.path.dirname(file_pref)
        file_name = os.path.basename(file_pref)

        doc = Document.create(file_name=file_name, file_location=file_location, file_extension=file_extension)
        doc_index_id_map[doc_index] = doc.document_id

    term_id_posting_map = {}
    for doc_index, doc_terms in enumerate(file_terms):
        term_freq_dict = {term_id_map[term]: freq for term, freq in dict(Counter(doc_terms)).items()}

        for term_id, freq in term_freq_dict.items():
            term_posting_dict = term_id_posting_map.setdefault(term_id, {})
            term_posting_dict[str(doc_index_id_map[doc_index])] = freq

    __update_postings(term_id_posting_map)
