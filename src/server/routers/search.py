from fastapi import APIRouter

from src.schemas.search import SearchRequest, SearchResponse
from src.server.services.search import get_query_results

search_router = APIRouter()

BASE = "/search"


@search_router.post(BASE, response_model=SearchResponse)
def query(request_body: SearchRequest):
    return get_query_results(request_body)
