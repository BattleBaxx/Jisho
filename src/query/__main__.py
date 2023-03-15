import sys

from src.query.doc_retriever import DocumentRetriever

if __name__ == "__main__":
    query_terms = sys.argv[1:]
    retriever = DocumentRetriever()
    print(retriever.retrieve_relevant_documents(query_terms))
