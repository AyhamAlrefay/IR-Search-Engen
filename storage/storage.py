import os
import pickle

class Storage:
    # Save and load functions for TF-IDF data
    @staticmethod
    def save_file(file_location: str, content):
        if os.path.exists(file_location):
            os.remove(file_location)
        with open(file_location, 'wb') as handle:
            pickle.dump(content, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_file(file_location: str):
        with open(file_location, 'rb') as handle:
            content = pickle.load(handle)
        return content

    @staticmethod
    def save_tfidf_data(tfidf_matrix, tfidf_model, name_dataset):
        folder_path = 'D:\ir-search-engine\storage'  # Replace with your actual folder path
        # Ensure the folder exists
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        # Save the files with dynamic names based on the dataset name
        save_file(os.path.join(folder_path, f"{name_dataset}_tfidf_matrix.pickle"), tfidf_matrix)
        save_file(os.path.join(folder_path, f"{name_dataset}_tfidf_model.pickle"), tfidf_model)

# Example usage:
# storage = Storage()
# storage.save_tfidf_data(tfidf_matrix, tfidf_model, 'my_dataset')
