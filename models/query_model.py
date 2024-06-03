from pydantic import BaseModel

class QueryModel(BaseModel):
    query_id: str
    text: str