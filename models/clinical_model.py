from pydantic import BaseModel

class ClinicalModel(BaseModel):
    doc_id: str
    title: str
    condition: str
    summary: str
    detailed_description: str
    eligibility: str