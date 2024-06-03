from sklearn.metrics.pairwise import cosine_similarity
from utils.storage.storage import Storage
from utils.helpers.get_doc_object import DatasetGetObjectData
from fastapi import APIRouter,HTTPException


class QueryMatchingRanking:
    def __init__(self, page, items_per_page, threshold):
        self.storage = Storage()
        self.page = page
        self.items_per_page = items_per_page
        self.threshold = threshold
        self.start_index = (page - 1) * self.items_per_page
        self.end_index = self.start_index + self.items_per_page

    def get_tfidf_results(self, dataset_name, query_vector):
        tfidf_matrix = Storage.load_file(f"{Storage.dir}\\{dataset_name}_tfidf_matrix.pickle")
        similarities = cosine_similarity(tfidf_matrix, query_vector).flatten()
        sorted_indices = similarities.argsort()[::-1][self.start_index:self.end_index]
            
        top_indices = []
        for i in sorted_indices:
            if similarities[i] >= self.threshold:
                top_indices.append(i.item())
                
        dataset_get_obj = DatasetGetObjectData(dataset_name)
        results = [dataset_get_obj.get_object_data(data) for data in top_indices]
        return results

    def get_word_embedding_results(self, dataset_name, query_vector):
        documents_vectors = Storage.load_file(f"{Storage.dir}\\{dataset_name}_documents_vectors.pickle")
        similarities = cosine_similarity(documents_vectors, query_vector).flatten()
        sorted_indices = similarities.argsort()[::-1][self.start_index:self.end_index]
        top_indices = []
        for i in sorted_indices:
            if similarities[i] >= self.threshold:
                top_indices.append(i.item())

        dataset_get_obj = DatasetGetObjectData(dataset_name)
        
        results = [dataset_get_obj.get_object_data(data) for data in top_indices]
        return results
