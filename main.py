from services.offline.offline_process_datasets.process_dataset import OfflineProcesses
from utils.constants import AppConstants
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.preprocessing.preprocessing_service import router as preprocessing_router
from services.online.query_representation.query_representation_service import router as query_representation_router
from services.online.query_matching.query_matching_ranking_service import router as query_matching_ranking_router
from services.online.online_services import router as online_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(preprocessing_router)
app.include_router(query_representation_router)
app.include_router(query_matching_ranking_router)
app.include_router(online_router)

def init():
    offline_processes = OfflineProcesses()
    #offline_processes.process_dataset(AppConstants.BEIR_QUERIES.value)
    #offline_processes.process_dataset(AppConstants.CLINICAL_QUERIES.value)
    #offline_processes.process_dataset(AppConstants.BEIR_DATASET.value)
    #offline_processes.process_dataset(AppConstants.CLINICAL_DATASET.value)
    offline_processes.process_dataset(AppConstants.BEIR_DATASET.value, tfidf = False)
    #offline_processes.process_dataset(AppConstants.CLINICAL_DATASET.value, tfidf = False)

init()
