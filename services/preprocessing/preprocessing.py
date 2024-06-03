import numpy as np
import re
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from spellchecker import SpellChecker
from num2words import num2words
import nltk
from static.country_symbols import country_symbols
from typing import List


class TextPreprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.spell_checker = SpellChecker()

    def convert_lower_case(self,data):
        return np.char.lower(data)

    def remove_stop_words(self,data):
        stop_words = stopwords.words('english')
        words = word_tokenize(str(data))
        new_text = ""
        for w in words:
            if w not in stop_words and len(w) > 1:
                new_text = new_text + " " + w
        return new_text

    def remove_punctuation(self,data):
        symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
        for i in range(len(symbols)):
            data = np.char.replace(data, symbols[i], ' ')
            data = np.char.replace(data, "  ", " ")
        data = np.char.replace(data, ',', '')
        return data
    
    def remove_apostrophe(self,data):
        return np.char.replace(data, "'", "")

    def stemming(self,data):
        stemmer= PorterStemmer()

        tokens = word_tokenize(str(data))
        new_text = ""
        for w in tokens:
            new_text = new_text + " " + stemmer.stem(w)
        return new_text

    def nltk_tag_to_wordnet_tag(nltk_tag):
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:
            return None

    def lemmatize(self, sentence):
        lemmatizer = WordNetLemmatizer()
        #tokenize the sentence and find the POS tag for each token
        nltk_tagged = nltk.pos_tag(word_tokenize(str(sentence)))
        #tuple of (token, wordnet_tag)
        wordnet_tagged = map(lambda x: (x[0], self.nltk_tag_to_wordnet_tag(x[1])), nltk_tagged)
        lemmatized_sentence = []
        for word, tag in wordnet_tagged:
            if tag is None:
                #if there is no available tag, append the token as is
                lemmatized_sentence.append(word)
            else:
                #else use the tag to lemmatize the token
                lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
        return " ".join(lemmatized_sentence)

    def convert_numbers(self,data):
        tokens = word_tokenize(str(data))
        new_text = ""
        for w in tokens:
            try:
                w = num2words(int(w))
            except:
                a = 0
            new_text = new_text + " " + w
        new_text = np.char.replace(new_text, "-", " ")
        return new_text

    def remove_urls(self,data):
        cleaned_text = re.sub(r'/(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?\/[a-zA-Z0-9]{2,}|((https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?)|(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})?/g', '', data)
        return cleaned_text;

    def correct_sentence_spelling(self,data):
        tokens = word_tokenize(str(data))
        misspelled =  self.spell_checker.unknown(tokens)
        for i, token in enumerate(tokens):
            if token in misspelled:
                corrected =  self.spell_checker.correction(token)
                if corrected is not None:
                    tokens[i] = corrected
        return " ".join(tokens)



    def replace_country_symbols(self,data):
    
        words = word_tokenize(data)
        replaced_words = [country_symbols[word] if word in country_symbols else word for word in words]
        return " ".join(replaced_words)

    def custom_tokenizer(text: str) -> List[str]:
        tokens = word_tokenize(text.lower())
        return tokens

    def preprocess_beir(self, data):
        data = self.remove_urls(data)
        data = self.convert_numbers(data)
        data = self.convert_lower_case(data)
        data = self.remove_punctuation(data)
        data = self.remove_apostrophe(data)
        data = self.remove_stop_words(data)
        return data

    def preprocess_clinicaltrials(self, data):
        data = self.convert_lower_case(data)
        data = self.remove_punctuation(data) 
        data = self.remove_apostrophe(data)
        data = self.remove_stop_words(data)
        data = self.stemming(data)
        data = self.convert_numbers(data)
        data = self.stemming(data)
        data = self.remove_punctuation(data)
        data = self.convert_numbers(data)
        data = self.stemming(data) 
        data = self.remove_punctuation(data)
        data = self.remove_stop_words(data) 
        return data
   