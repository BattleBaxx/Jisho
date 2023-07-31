from datetime import datetime

from pydantic import BaseModel


class SearchBase(BaseModel):
    query: str


class SearchRequest(SearchBase):
    extension: str | None = None
    min_size: int | None = None
    max_size: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    file_location: str | None = None


class DocumentRelevance(BaseModel):
    file_name: str
    file_location: str
    file_extension: str
    user: str
    size: str
    modified: datetime
    relevance: float


class SearchResponse(SearchBase):
    doc_list: list[DocumentRelevance]
