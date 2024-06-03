from utils.constants import AppConstants
from fastapi import HTTPException

@staticmethod
def check_if_dataset_exists(dataset_name):
    if (dataset_name != AppConstants.CLINICAL_DATASET.value and
        dataset_name != AppConstants.CLINICAL_QUERIES.value and
        dataset_name != AppConstants.BEIR_DATASET.value and
        dataset_name != AppConstants.BEIR_QUERIES.value):
        raise HTTPException(
            status_code=400,
            detail="The dataset Requested is not found"
        )