from fastapi import APIRouter,HTTPException
import pandas as pd
from services.online.query_representation.query_representation import QueryRepresentation
from models.query import Query
import httpx
from utils.constants import AppConstants
from utils.helpers.check_if_dataset_exists import check_if_dataset_exists
from gensim.utils import simple_preprocess


router = APIRouter(
    prefix='/query-representation',
    tags = ['Query Representation']
)


@router.post("")
async def query_representation(query: Query):
    check_if_dataset_exists(query.dataset_name)
    data = query.query
    payload = {'query': data, 'dataset_name': query.dataset_name, "spell_check": query.spell_check,"tf_idf": query.tf_idf}
    if(query.spell_check):
        url = f"{AppConstants.BASE_URL.value}/preprocess/spell-check"
        async with httpx.AsyncClient() as client:
            response = await client.post(url,json=payload,timeout=httpx.Timeout(50))
            data = response.json()['corrected_data']
    if(query.tf_idf): 
        url = f"{AppConstants.BASE_URL.value}/preprocess/process-data"
        async with httpx.AsyncClient() as client:
            payload = {'query': data, 'dataset_name': query.dataset_name, "spell_check": query.spell_check,"tf_idf": query.tf_idf}
            response = await client.post(url,
                                         json=payload,
                                         timeout=httpx.Timeout(50))
            data = response.json()['processed_data']
        
        return {
            'vector': pd.Series(
                QueryRepresentation.tfidf_vectorize_query(data, query.dataset_name)
            ).to_json(orient='values')
        }
    else:
        #url = f"{AppConstants.BASE_URL.value}/preprocess/process-data"
        data = simple_preprocess(query.query)
        # payload = {'query': data, 'dataset_name': query.dataset_name, "spell_check": query.spell_check,"tf_idf": query.tf_idf}
        # async with httpx.AsyncClient() as client:
        #     response = await client.post(url,
        #                                  json=payload,
        #                                  timeout=httpx.Timeout(50))
            
        # data = response.json()['processed_data']

        # get_inp_url = f"{AppConstants.BASE_URL}/preprocess/tokenize"
        # async with httpx.AsyncClient() as client:
        #     response = await client.post(get_inp_url, json={'query': response.json()['cleaned_text']},
        #                                  timeout=httpx.Timeout(100.0)
        #                                  )

        return {
            'vector': pd.Series(
                QueryRepresentation.word_embedding_vectorize_query(
                    data, query.dataset_name
                )).to_json(orient='values')
        }


@router.post("/query-refinement")
async def query_representation(query: Query):
    check_if_dataset_exists(query.dataset_name)
    
    # url = f"{AppConstants.BASE_URL}/preprocess/spell-check"
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(url,
    #                                     json={'query': query},
    #                                     timeout=httpx.Timeout(50))
    # data = response.json()['corrected']
    return {
        'vector': pd.Series(
            QueryRepresentation.tfidf_vectorize_query(query.query, query.dataset_name)
        ).to_json(orient='values')
    }
