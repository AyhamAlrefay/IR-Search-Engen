from sklearn.feature_extraction.text import TfidfVectorizer
from utils.storage.storage import Storage
from services.offline.tf_idf_indexing.tf_idf_indexing import TfidfProcessor
from services.preprocessing.preprocessing import TextPreprocessor
from utils.datasets.datasets_loader import DatasetsLoader
from utils.constants import AppConstants
from services.offline.word_embeddings_indexing.word_embedding_indexing import WordEmbeddingProcessor

class OfflineProcesses:
    def __init__(self):
        self.pre_process = TextPreprocessor()
        self.tfidf = TfidfProcessor()
        self.storage = Storage()

    def process_dataset(self, name_dataset, tfidf = True):
        documents, dataset = DatasetsLoader.load_datasource(name_dataset)
        if (name_dataset == AppConstants.CLINICAL_DATASET.value):
            if(tfidf):
                self._process_clinical_tfidf(documents)
            else:
                self._process_clinical_w2v()
        elif (name_dataset == AppConstants.BEIR_DATASET.value):
            if(tfidf):
                self._process_beir_tfidf(dataset)
            else:
                self._process_beir_w2v()
        elif (name_dataset == AppConstants.CLINICAL_QUERIES.value or name_dataset == AppConstants.BEIR_QUERIES.value):
            self._process_queries(documents, name_dataset)
        else:
            print("No such datasets")

    def _process_queries(self, queries, name_dataset):
        self.tfidf.fit_transform(queries)
        tfidf_matrix = self.tfidf.get_tfidf_matrix()
        tfidf_model = self.tfidf.get_tfidf_model()
        Storage.save_tfidf_data(tfidf_matrix = tfidf_matrix, tfidf_model = tfidf_model, name_dataset= name_dataset)
        print("The queries are processing and storage of the tfidf_matrix and tfidf_model.")
        
    def _process_clinical_tfidf(self, documents):
        documents_processor = [self.pre_process.preprocess_clinicaltrials(doc) for doc in documents]
        self.tfidf.fit_transform(documents_processor)
        tfidf_matrix = self.tfidf.get_tfidf_matrix()
        tfidf_model = self.tfidf.get_tfidf_model()
        Storage.save_tfidf_data(tfidf_matrix = tfidf_matrix, tfidf_model = tfidf_model, name_dataset= AppConstants.CLINICAL_DATASET.value)
        print("The dataset clinicaltrials are processing and storage of the tfidf_matrix and tfidf_model.")
        
    def _process_beir_tfidf(self, dataset):
        doc_ids = []
        titles = []
        texts = []
        stances = []
        urls = []

        for doc in dataset.docs_iter():
            doc_ids.append(doc.doc_id)
            titles.append(doc.title)
            texts.append(doc.text)
            stances.append(doc.stance)
            urls.append(doc.url)

        # Preprocess the corpus
        preprocessed_titles = [self.pre_process.preprocess_beir(title) for title in titles]
        preprocessed_texts = [self.pre_process.preprocess_beir(text) for text in texts]
        preprocessed_stances = [self.pre_process.preprocess_beir(description) for description in stances]
        preprocessed_urls = [self.pre_process.preprocess_beir(url) for url in urls]

        # Save preprocessed data to a file
        preprocessed_corpus = {
            'titles': preprocessed_titles,
            'texts': preprocessed_texts,
            'stances': preprocessed_stances,
            'urls': preprocessed_urls
        }

        # Fit the vectorizer on the combined corpus
        vectorizer = TfidfVectorizer()
        vectorizer.fit(preprocessed_corpus['titles'] + preprocessed_corpus['texts'] +
                       preprocessed_corpus['stances'] + preprocessed_corpus['urls'])

        # Transform each column separately
        tfidf_titles = vectorizer.transform(preprocessed_corpus['titles'])
        tfidf_texts = vectorizer.transform(preprocessed_corpus['texts'])
        tfidf_stances = vectorizer.transform(preprocessed_corpus['stances'])
        tfidf_urls = vectorizer.transform(preprocessed_corpus['urls'])

        # Define weights for each column
        weights = {
            'title': 4,
            'text': 5,
            'stance': 3,
            'url': 2
        }

        # Combine vectors with weights
        tfidf_matrix = (
            weights['title'] * tfidf_titles +
            weights['text'] * tfidf_texts +
            weights['stance'] * tfidf_stances +
            weights['url'] * tfidf_urls
        )/(weights['title'] + weights['text'] + weights['stance'] + weights['url'])
        tfidf_model = vectorizer

        Storage.save_tfidf_data(tfidf_matrix = tfidf_matrix, tfidf_model = tfidf_model, name_dataset= AppConstants.BEIR_DATASET.value)
        print("The dataset beir are processing and storage of the tfidf_matrix and tfidf_model.")
        
    def _process_clinical_w2v(self):
        WordEmbeddingProcessor(500, 1, 4, 35,AppConstants.CLINICAL_DATASET.value).train_model()
        print("The dataset clinical are processing and storage of the w2v_matrix and w2v_model.")

        
    def _process_beir_w2v(self):
        WordEmbeddingProcessor(500, 1, 3, 35,AppConstants.BEIR_DATASET.value).train_model()
        print("The dataset beir are processing and storage of the w2v_matrix and w2v_model.")
