from pydantic import BaseModel


class Query(BaseModel):
    query: str
    dataset_name: str
    spell_check: bool = True
    tf_idf: bool = True
