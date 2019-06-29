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

    #SAVE THE DICTIONARY AND THE CORPUS#
    if not os.path.exists('General'):
        os.makedirs('General')
    dict_of_tokens.save('General/myDict.dict')
    corpora.MmCorpus.serialize('General/myCorpus.mm', corpus_of_tokens)
    #loaded_dict = corpora.Dictionary.load('General/myDict.dict')
    #loaded_corpus = corpora.MmCorpus('General/myCorpus.mm')

    #LDA#
    topic_number = 60
    lda_model = LdaModel(corpus = corpus_of_tokens,
                             id2word = dict_of_tokens,
                             num_topics = topic_number,
                             iterations = 50,
                             passes = 5,
                             decay = 0.5)
    lda_model.save('General/lda_model.model')
    with open('General/lda_topics.txt', 'w') as lda_topics:
        for item in lda_model.print_topics(-1):
            print(item, file = lda_topics, flush = True)
    #lda_load_model = LdaModel.load('General/lda_model.model')

    #LSA#
    lsa_model = LsiModel(corpus = corpus_of_tokens,
                             id2word = dict_of_tokens,
                             num_topics = topic_number,
                             decay = 0.5)
    lsa_model.save('General/lsa_model.model')
    #lsa_load_model = LsaModel.load('General/lsa_model.model')
    with open('General/lsa_topics.txt', 'w') as lsa_topics:
        print(*lsa_model.print_topics(-1), file = lsa_topics, sep = '\n', flush = True)
    
