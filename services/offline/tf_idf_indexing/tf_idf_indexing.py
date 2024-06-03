from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

class TfidfProcessor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = None
        self.tfidf_model = None
        self.df = None

    def fit_transform(self, preprocessed_documents):
        # Fit and transform the preprocessed documents
        self.tfidf_matrix = self.vectorizer.fit_transform(preprocessed_documents)
        # Create a DataFrame from the new TF-IDF matrix
        #self.df = pd.DataFrame.sparse.from_spmatrix(self.tfidf_matrix, columns=self.vectorizer.get_feature_names_out(), index=corpus.keys())
        # Update the tfidf_model variable
        self.tfidf_model = self.vectorizer

    def get_tfidf_matrix(self):
        return self.tfidf_matrix

    def get_tfidf_model(self):
        return self.tfidf_model

# Example usage:
# processor = TfidfProcessor()
# processor.fit_transform(preprocessed_documents, corpus)
# tfidf_df = processor.get_dataframe()
# tfidf_model = processor.get_tfidf_model()
