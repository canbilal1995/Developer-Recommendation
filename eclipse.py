#@Author: Bilal CAN

import csv
import os
from gensim.models import LdaModel, LsiModel
from gensim.models.coherencemodel import CoherenceModel
from gensim import corpora
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

if __name__ == "__main__":
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
    en_stop.add('eclipse')
    en_stop.add('error')
    en_stop.add('project')
    p_stemmer = PorterStemmer()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = []
    for element in range(len(texts)):
        sub_tokens = []
        for word in range(len(texts[element])):
            sub_tokens += tokenizer.tokenize(texts[element][word]) #atomic words are gathered from each word
            stopped_sub_tokens = [i for i in sub_tokens if not i in en_stop] #stopwords are discarded
            stemmed_sub_tokens = [p_stemmer.stem(i) for i in stopped_sub_tokens] #stemming
        tokens += [stemmed_sub_tokens]

    dict_of_tokens = corpora.Dictionary() #Dictionary object is created
    corpus_of_tokens = [dict_of_tokens.doc2bow(doc, allow_update = True) for doc in tokens] #corpus is created

    if not os.path.exists('General'):
        os.makedirs('General')
    dict_of_tokens.save('General/myDict.dict')
    corpora.MmCorpus.serialize('General/myCorpus.mm', corpus_of_tokens)
