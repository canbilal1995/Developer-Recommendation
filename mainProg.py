#@Author: Bilal CAN

import csv
import os.path
from gensim import corpora
from gensim.models import LsiModel
from gensim.models.coherencemodel import CoherenceModel
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import matplotlib.pyplot as plt

texts = []
with open('Results/collected_data.csv', 'r') as collected_data:
    reader = csv.reader(collected_data, delimiter = '\t')
    count_line = 0
    for row in reader:
        if count_line == 0:
            count_line += 1
            continue
        else:
            count_line += 1
            texts += [row[3].strip().split()]
            
en_stop = set(stopwords.words('english')) #stopwords
# en_stop += [] #after the first run of LDA and LSA words with too high frequencies are eliminated
p_stemmer = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')
tokens = []
for element in range(len(texts)):
    sub_tokens = []
    for word in range(len(texts[element])):
        texts[element][word] = texts[element][word].lower()
        sub_tokens += tokenizer.tokenize(texts[element][word]) #atomic words are gathered from each word
        stopped_sub_tokens = [i for i in sub_tokens if not i in en_stop] #stopwords are discarded
        stemmed_sub_tokens = [p_stemmer.stem(i) for i in stopped_sub_tokens] #stemming
    tokens += [stemmed_sub_tokens]
