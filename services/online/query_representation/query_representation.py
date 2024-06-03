import numpy as np
from utils.storage.storage import Storage
from gensim.utils import simple_preprocess

class QueryRepresentation:

    @staticmethod
    def tfidf_vectorize_query(query, dataset_name):
        path = f"{Storage.dir}\\{dataset_name}_tfidf_model.pickle"
        model = Storage.load_file(path)
        return model.transform([query]).toarray()[0]

    @staticmethod
    def word_embedding_vectorize_query(query, dataset_name):
        path = f"{Storage.dir}\\{dataset_name}_word2vec_model.model"
        model = Storage.load_file(path)

        vectors = []
        zero_vector = np.zeros(model.wv.vector_size)

        for token in query:
            if token in model.wv:
                try:
                    vectors.append(model.wv[token])
                except KeyError:
                    vectors.append(np.random(model.wv.vector_size))
        if vectors:
            vectors = np.asarray(vectors)
            query_vector = vectors.mean(axis=0)
        else:
            query_vector = zero_vector
            
        return query_vector
