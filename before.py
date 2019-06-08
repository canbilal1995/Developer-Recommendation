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

for element in range(len(texts)):
    for word in range(len(texts[element])):
        texts[element][word] = texts[element][word].lower()
