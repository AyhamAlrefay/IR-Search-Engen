from gensim.models import Word2Vec
from utils.datasets.datasets_loader import DatasetsLoader
import numpy as np
from utils.storage.storage import Storage
from gensim.utils import simple_preprocess

class WordEmbeddingProcessor:
    def __init__(self, vector_size, sg, workers, epochs, dataset_name):
        self.vector_size = vector_size
        self.sg = sg
        self.workers = workers
        self.epochs = epochs
        self.word_embedding_model = None
        self.documents_vectors = None
        self.dataset_name = dataset_name

    def init_sentences(self):
        sentences = []
        documents, _ = DatasetsLoader.load_datasource(self.dataset_name)
        for document in documents:
            sentences.append(
                simple_preprocess(document)
            )

        return sentences

    def train_model(self):
        sentences = self.init_sentences()
        model = Word2Vec(sentences,
                         vector_size=self.vector_size,
                         sg=self.sg,
                         workers=self.workers,
                         epochs=self.epochs)

        self.word_embedding_model = model
        self.documents_vectors = self.vectorize_documents(sentences)
        self.save_model()

    def vectorize_documents(self, sentences):
        documents_vectors = []
        for sentence in sentences:
            zero_vector = np.zeros(self.vector_size)
            vectors = []
            for token in sentence:
                if token in self.word_embedding_model.wv:
                    try:
                        vectors.append(self.word_embedding_model.wv[token])
                    except KeyError:
                        vectors.append(np.random(self.vector_size))
            if vectors:
                vectors = np.asarray(vectors)
                avg_vec = vectors.mean(axis=0)
                documents_vectors.append(avg_vec)
            else:
                documents_vectors.append(zero_vector)
        return documents_vectors

    def save_model(self):
        Storage.save_word_embedding_data(documents_vectors= self.documents_vectors,word_embedding_model= self.word_embedding_model,name_dataset = self.dataset_name)
