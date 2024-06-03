import httpx
from fastapi import APIRouter
from fastapi import HTTPException
from models.query import Query
from utils.constants import AppConstants

router = APIRouter(
    tags=["Online Service"]
)

@router.post("/search")
async def search(page: int ,body: Query):
    url = f"{AppConstants.BASE_URL.value}/query-representation"
    data = body.query
    payload = {'query': data, 'dataset_name': body.dataset_name, "spell_check": body.spell_check,"tf_idf": body.tf_idf}
    async with httpx.AsyncClient() as client:
        response = await client.post(url,
                                     json=payload,
                                     timeout=httpx.Timeout(50.0))
            
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    url = f"{AppConstants.BASE_URL.value}/query-match?page=" + \
                  str(page) + "&dataset_name=" + \
                  str(body.dataset_name) + "&tfidf=" + \
                  str(body.tf_idf)
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=response.json(), timeout=httpx.Timeout(50.0))

    return {'results': response.json()}


@router.post("/query-suggestion")
async def search(body: Query):
    get_inp_url = f"{AppConstants.BASE_URL.value}/query-representation/query-refinement"
    data = body.query
    payload = {'query': data, 'dataset_name': body.dataset_name, "spell_check": body.spell_check,"tf_idf": body.tf_idf}
    async with httpx.AsyncClient() as client:
        response = await client.post(get_inp_url,
                                     json=payload,
                                     timeout=httpx.Timeout(50.0))
    

    get_inp_url = f"{AppConstants.BASE_URL.value}/query-match?page=1" + \
                  "&dataset_name=" + \
                  str(body.dataset_name) + "&tfidf=True"
    async with httpx.AsyncClient() as client:
        response = await client.post(get_inp_url, json=response.json(), timeout=httpx.Timeout(50.0))

    return {'results': response.json()}
