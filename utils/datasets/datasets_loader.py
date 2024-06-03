import ir_datasets
from utils.constants import AppConstants

class DatasetsLoader:
    
    @staticmethod
    def load_datasource(dataset_name):
        return DatasetsLoader.dataset_to_documnets(dataset_name)
    
    @staticmethod
    def dataset_to_documnets(dataset_name):
        if(AppConstants.CLINICAL_DATASET.value == dataset_name):
            clinicaltrials = ir_datasets.load("clinicaltrials/2021/trec-ct-2021")
            documents = []
            for doc in clinicaltrials.docs_iter():
                documents.append(doc.title + " " + doc.summary + " " + doc.detailed_description + " " + doc.eligibility)
            return documents, clinicaltrials
        
        elif(AppConstants.BEIR_DATASET.value == dataset_name):
            beir = ir_datasets.load("beir/webis-touche2020/v2")
            documents = []
            for doc in beir.docs_iter():
                documents.append(doc.title + " " + doc.text + " " + doc.stance + " " + doc.url)
            return documents, beir
        
        if(AppConstants.CLINICAL_QUERIES.value == dataset_name):
            clinicaltrials = ir_datasets.load("clinicaltrials/2021/trec-ct-2021")
            queries = []
            for query in clinicaltrials.queries_iter():
                queries.append(query.text)
            return queries, clinicaltrials
        
        elif(AppConstants.BEIR_QUERIES.value == dataset_name):
            beir = ir_datasets.load("beir/webis-touche2020/v2")
            queries = []
            for query in beir.queries_iter():
                queries.append(query.text)
            return queries, beir
        
        else:
            print("No Such Dataset")
            return None
        
    @staticmethod
    def get_dataset(dataset_name):
        if(AppConstants.CLINICAL_DATASET.value == dataset_name or AppConstants.CLINICAL_QUERIES.value == dataset_name):
            clinicaltrials = ir_datasets.load("clinicaltrials/2021/trec-ct-2021")
            return clinicaltrials
        
        elif(AppConstants.BEIR_DATASET.value == dataset_name or AppConstants.BEIR_QUERIES.value == dataset_name):
            beir = ir_datasets.load("beir/webis-touche2020/v2")
            return beir
        
        else:
            print("No Such Dataset")
            return None