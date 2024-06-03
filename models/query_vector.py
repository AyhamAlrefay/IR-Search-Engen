from pydantic import BaseModel

class QueryVector(BaseModel):
    vector: str
