from src.query.doc_retriever import DocumentRetriever
from src.schemas.search import SearchRequest, SearchResponse


def get_query_results(query_data: SearchRequest) -> SearchResponse:
    retriever = DocumentRetriever()
    documents = retriever.retrieve_relevant_documents(query_data)
    return SearchResponse(query=query_data.query, doc_list=documents)
