from fastapi import APIRouter
from services.preprocessing.preprocessing import TextPreprocessor
from utils.constants import AppConstants
from models.query import Query

router = APIRouter(
    prefix='/preprocess',
    tags = ['Preprocess Data']
)

@router.post("/process-data")
async def preprocess_data(query: Query):
    if query.dataset_name == AppConstants.CLINICAL_DATASET.value:
        return {'processed_data': TextPreprocessor().preprocess_clinicaltrials(query.query)}
    else:
        return {'processed_data': TextPreprocessor().preprocess_beir(query.query)}

@router.post("/spell-check")
async def tokenize_text(query: Query):
    return {'corrected_data': TextPreprocessor().correct_sentence_spelling(query.query)}