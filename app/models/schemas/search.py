from pydantic import BaseModel
from typing import List

class WebSearchQuery(BaseModel):
    query: str

class WebSearchResult(BaseModel):
    query: str
    links: List[str]
    answers: List[str]
