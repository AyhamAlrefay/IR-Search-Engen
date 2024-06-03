import json
from fastapi import APIRouter,HTTPException
from services.online.query_matching.query_matching_ranking import QueryMatchingRanking
from models.query_vector import QueryVector

router = APIRouter(
    prefix='/query-match',
    tags = ['Query Matching And Ranking']
)

@router.post("")
async def search(page: int, dataset_name: str, body: QueryVector, tfidf: bool = True):
    if tfidf:
        return  QueryMatchingRanking(page, 10, 0.1).get_tfidf_results(dataset_name, [json.loads(body.vector)])

    else:
        return QueryMatchingRanking(page, 10, 0.1).get_word_embedding_results(dataset_name,[json.loads(body.vector)])
