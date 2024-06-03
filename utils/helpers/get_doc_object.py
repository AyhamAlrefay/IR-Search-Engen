from utils.datasets.datasets_loader import DatasetsLoader
from utils.constants import AppConstants
from models.beir_model import BeirModel
from models.clinical_model import ClinicalModel
from models.query_model import QueryModel

class DatasetGetObjectData:
    def __init__(self, dataset_name):
        self.dataset = DatasetsLoader.get_dataset(dataset_name)
        self.dataset_name = dataset_name
    
    def get_object_data(self, index):
        if self.dataset_name == AppConstants.BEIR_DATASET.value:
            data = self.dataset.docs_iter()[index]
            return BeirModel(doc_id= data.doc_id, title = data.title, text= data.text, stance= data.stance,url=data.url)
        elif self.dataset_name == AppConstants.CLINICAL_DATASET.value:
            data = self.dataset.docs_iter()[index]
            return ClinicalModel(doc_id=data.doc_id,title=data.title,condition=data.condition,summary = data.summary,detailed_description=data.detailed_description,eligibility=data.eligibility)
        elif self.dataset_name == AppConstants.CLINICAL_QUERIES.value or self.dataset_name == AppConstants.BEIR_QUERIES.value:
            i = 0
            for query in self.dataset.queries_iter():
                if (i == index ):
                    return QueryModel(query_id=query.query_id,text = query.text)
                i+=1
            return None
        else:
            return None