
import sys
import os
sys.path.append('D:/ir-search-engine/services/preprocessing')
sys.path.append('D:/ir-search-engine/services/offline/indexing')
sys.path.append('D:/ir-search-engine/storage')
import tf_idf_indexing
import preprocessing
import storage


def process_dataset(dataset,name_dataset):
    pre=preprocessing.TextPreprocessor()
    tfidf=tf_idf_indexing.TfidfProcessor()
    # stor= storage.Storage()
    stor=storage.Storage()
    if(name_dataset=="clinicaltrials"):
        documents,corpus=dataset_to_documnets(name_dataset,dataset)
        documents_processor=[pre.preprocess_clinicaltrials(doc) for doc in documents] 
        tfidf.fit_transform(documents_processor,corpus)
        tfidf_matrix= tfidf.get_tfidf_matrix
        tfidf_model= tfidf.get_tfidf_model
        stor.save_tfidf_data(tfidf_matrix,tfidf_model,name_dataset)
        print("The dataset clinicaltrials are processing and storage of the tfidf_matrix and tfidf_model.")
    
    else: 
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
                
        # Define the corpus as a dictionary with doc_id as the key
        corpus = {
            doc_ids[i]: {
                'title': titles[i],
                'text': texts[i],
                'stance': stances[i],
                'url': urls[i]
            } for i in range(len(doc_ids))
        }
        # Preprocess the corpus
        preprocessed_titles = [pre.preprocess_beir(title) for title in titles]
        preprocessed_texts = [pre.preprocess_beir(text) for text in texts]
        preprocessed_stances = [pre.preprocess_beir(stance) for stance in stances]
        preprocessed_urls = [pre.preprocess_beir(url) for url in urls]

        # Save preprocessed data to a file
        preprocessed_corpus = {
            'titles': preprocessed_titles,
            'texts': preprocessed_texts,
            'stances': preprocessed_stances,
            'urls': preprocessed_urls
        }

        # Fit the vectorizer on the combined corpus
        vectorizer = TfidfVectorizer()
        vectorizer.fit(preprocessed_corpus['titles'] + preprocessed_corpus['texts'] + preprocessed_corpus['stances'] + preprocessed_corpus['urls'])

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
        )/( weights['title'] + weights['text'] + weights['stance'] +  weights['url'] )
        tfidf_model = vectorizer        
        
        stor.save_tfidf_data(tfidf_matrix,tfidf_model,name_dataset)
        print("The dataset beir are processing and storage of the tfidf_matrix and tfidf_model.")
        print(name_dataset)
    
    
    
    
    
def dataset_to_documnets(name_dataset,dataset):
    if(name_dataset=="clinicaltrials"):
       corpus = {}
       for doc in dataset.docs_iter():
           corpus[doc.doc_id] = doc.title + " " + doc.summary + " " + doc.detailed_description + " " + doc.eligibility
       documents = list(corpus.values())
       return documents,corpus
    else:
        corpus = {}
        for doc in dataset.docs_iter():
           corpus[doc.doc_id] = doc.title + " " + doc.text + " " + doc.stance + " " + doc.url
        documents = list(corpus.values())
        return documents,corpus
    
    
    


def process_query(query: str, tfidf_model, tfidf_matrix):
    query_tfidf = tfidf_model.transform([query])
    cosine_similarities = cosine_similarity(query_tfidf, tfidf_matrix).flatten()
    ranked_doc_indices = cosine_similarities.argsort()[::-1]
    return ranked_doc_indices, cosine_similarities




def getRetrievedQueries(name_dataset,tfidf_model,tfidf_matrix,query: str, k=10):
    pre=preprocessing.TextPreprocessor()
    preprocessed_query=""
    if(name_dataset=="beir"):
        preprocessed_query = pre.preprocess_beir(query)
    else:
        preprocessed_query = pre.preprocess_clinicaltrials(query)
    ranked_indices, _ = process_query(preprocessed_query, tfidf_model, tfidf_matrix)
    idsList = []
    for idx in ranked_indices[:k]:
        doc_id = list(corpus.keys())[idx]
        idsList.append(doc_id)
    return idsList




def calculate_recall_precision(query_id,dataset):
    relevant_docs = []
    for qrel in dataset.qrels_iter():
        if qrel[0] == query_id and qrel[2] > 0:
            relevant_docs.append(qrel[1])

    retrieved_docs = []
    for query in dataset.queries_iter():
        if query[0] == query_id:
            retrieved_docs = getRetrievedQueries(query[1])
            break  

    y_true = [1 if doc_id in relevant_docs else 0 for doc_id in retrieved_docs]
    true_positives = sum(y_true)
    recall_at_10 = true_positives / len(relevant_docs) if relevant_docs else 0
    precision_at_10 = true_positives / 10
    print(f"Query ID:  {query_id}, Recall@10: {recall_at_10}")
    print(f"Query ID: {query_id}, Precision@10: {precision_at_10}")    
    return recall_at_10



def calculate_MAP(query_id,dataset):
    relevant_docs = []
    for qrel in dataset.qrels_iter():
        if qrel[0] == query_id and qrel[2] > 0:
            relevant_docs.append(qrel[1])

    retrieved_docs = []
    for query in dataset.queries_iter():
        if query[0] == query_id:
            retrieved_docs = getRetrievedQueries(query[1])
            break

    pk_sum = 0

    total_relevant = 0

    for i in range(1, 11):
        relevant_ret = 0

        for j in range(i):
            if j < len(retrieved_docs) and retrieved_docs[j] in relevant_docs:
                relevant_ret += 1
        p_at_k = (relevant_ret / i) * (1 if i - 1 < len(retrieved_docs) and retrieved_docs[i - 1] in relevant_docs else 0)

        pk_sum += p_at_k

        if i - 1 < len(retrieved_docs) and retrieved_docs[i - 1] in relevant_docs:
            total_relevant += 1

    return 0 if total_relevant == 0 else pk_sum / total_relevant



def result_MAP(dataset):
    queries_ids = {qrel[0]: '' for qrel in dataset.qrels_iter()}
    map_sum = 0
    for query_id in list(queries_ids.keys()):
        map_sum += calculate_MAP(query_id)
    # print(f"Mean Average Precision (MAP@10): {map_sum / len(queries_ids)}")
    return map_sum / len(queries_ids)



def calculate_MRR(query_id,dataset):
    relevant_docs = []
    for qrel in dataset.qrels_iter():
        if qrel[0] == query_id and qrel[2] > 0:
            relevant_docs.append(qrel[1])

    retrieved_docs = []
    for query in dataset.queries_iter():
        if query[0] == query_id:
            retrieved_docs = getRetrievedQueries(query[1])
            break

    for i in range(1, 11):
        if retrieved_docs[i-1] in relevant_docs:
            return 1 / i
    return 0


def result_MRR(dataset):
    queries_ids = {qrel[0]: '' for qrel in dataset.qrels_iter()}
    queries_list = list(queries_ids.keys())
    mrr_sum = 0
    for query_id in queries_list:
        mrr_sum += calculate_MRR(query_id)
    # print(f"Mean Reciprocal Rank (MRR): {(1 / len(queries_list)) * mrr_sum}")
    return (1 / len(queries_list)) * mrr_sum