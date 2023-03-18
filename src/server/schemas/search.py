from datetime import datetime

from pydantic import BaseModel

from src.query.doc_retriever import DocRelevance


class SearchBase(BaseModel):
    query: str


class SearchRequest(SearchBase):
    extension: str | None = None
    min_size: int | None = None
    max_size: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    file_location: str | None = None


class SearchResponse(SearchBase):
    doc_List: list[DocRelevance]
