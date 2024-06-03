import os
import pickle

class Storage:
    dir = os.path.dirname(os.path.abspath(__file__)) + "\..\..\storage"
    def __init__(self):
        self.dir = os.path.dirname(os.path.abspath(__file__)) + "\..\..\storage"
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
            
    @staticmethod
    def save_file(file_location, content):
        if os.path.exists(file_location):
            os.remove(file_location)
        with open(file_location, 'wb') as handle:
            pickle.dump(content, handle, protocol=pickle.HIGHEST_PROTOCOL)


    @staticmethod
    def load_file(file_location):
        with open(file_location, 'rb') as handle:
            content = pickle.load(handle)
        return content

    @staticmethod
    def save_tfidf_data(tfidf_matrix, tfidf_model, name_dataset):
        # Save the files with dynamic names based on the dataset name
        Storage.save_file(os.path.join(Storage.dir, f"{name_dataset}_tfidf_matrix.pickle"), tfidf_matrix)
        Storage.save_file(os.path.join(Storage.dir, f"{name_dataset}_tfidf_model.pickle"), tfidf_model)
    
    @staticmethod
    def save_word_embedding_data(documents_vectors, word_embedding_model, name_dataset):
        # Save the files with dynamic names based on the dataset name
        Storage.save_file(os.path.join(Storage.dir, f"{name_dataset}_documents_vectors.pickle"), documents_vectors)
        Storage.save_file(os.path.join(Storage.dir, f"{name_dataset}_word2vec_model.model"), word_embedding_model)

# Example usage:
# storage = Storage()
# storage.save_tfidf_data(tfidf_matrix, tfidf_model, 'my_dataset')
