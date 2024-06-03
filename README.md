# IR-Search-Engen

The repository will guide you step by step to create your first basic search engine based on TF-IDF and word embedding techniques

## Used datasets

- Clinicaltrials 2021
- Beir/webis-touche2020/v2

## Project Services

- Online service
- Preprocessing service
- Query representation service
- Query matching and ranking service

## Flow of control

- The frontend interacts directly with online service to get the query results
- The online service forwards the query to the query representation service
- The representation service requests the preprocessing service to clean and correct the query
- The representation service accesses the trained models files to generate the query vector
- The flow returns to the online service where it forwards the query vector to the matching and ranking service
- The matching service measures the distance between the query vectors and the documents vectors
- The top results are selected as relevant answers for the targeted page
- The matching service queries the data from dataset to get the documents content
- The documents are sorted based on the Cosine similarity

## How to train the models

By accessing the offline service folder you will find two indexing folders:

- TF-IDF folder to train your model based on TF-IDF technique by using the TfidfVectorizer from Sklearn library
- Word embedding folder to train your model based on Word2Vec from Gensim library
- Change the locations in the Storage class to target your own local files
- Offline processor do all these trainning bassed on passed dataset name and indexing method

## Used libraries and packages

- FastApi
- NLTK
- Pandas
- Numpy
- Sklearn
- Gensim
  You will find the full list in the requirements file, all you have to do is pip install -r requirements.txt

## Authors

- Ayham Alrefaai
- Nour Aldin Alteilouny
- Ammar refaaia
- Mohamad Mu'yead Younes

## Damascus University - IR - 2024
