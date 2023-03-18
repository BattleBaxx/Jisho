from src.query.doc_retriever import DocumentRetriever
from src.server.schemas.search import SearchResponse


def get_query_results(query_data: dict) -> SearchResponse:
    retriever = DocumentRetriever()
    return SearchResponse(
        query=query_data["query"],
        doc_list=retriever.retrieve_relevant_documents(query_data)
    )