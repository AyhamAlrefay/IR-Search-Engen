from pydantic import BaseModel

class BeirModel(BaseModel):
    doc_id: str
    title: str
    text: str
    stance: str
    url: str
