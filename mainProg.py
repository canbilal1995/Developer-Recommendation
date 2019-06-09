#@Author: Bilal CAN

import csv
import os
from gensim.models import LdaModel, LdaMulticore, LsiModel
from gensim import corpora
from gensim.models import LsiModel
from gensim.models.coherencemodel import CoherenceModel
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import matplotlib.pyplot as plt

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
    counter_dict = {}
    for element in range(len(texts)):
        for word in range(len(texts[element])):
            texts[element][word] = texts[element][word].lower()
            if texts[element][word] in counter_dict:
                counter_dict[texts[element][word]] += 1
            else:
                counter_dict[texts[element][word]] = 1
    word_freq_list = sorted(counter_dict.items(), key=lambda a : a[1], reverse=True)
    with open('Results/word_freq.txt', 'w') as word_freq_txt:
        for word in word_freq_list:
            print("{}\t{}".format(word[0], word[1]), file = word_freq_txt, flush = True)
            
    en_stop = set(stopwords.words('english')) #stopwords
# en_stop += [] #after the first run of LDA and LSA words with too high frequencies are eliminated
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

    if not os.path.exists('TopicModelling'):
        os.makedirs('TopicModelling')
    dict_of_tokens.save('TopicModelling/myDict.dict')
    corpora.MmCorpus.serialize('TopicModelling/myCorpus.mm', corpus_of_tokens) 

    lda_model = LdaModel(corpus = corpus_of_tokens,
                     id2word = dict_of_tokens,
                     num_topics = 10,
                     iterations = 10,
                     passes = 5,
                     decay = 0.5)
    lda_model.save('TopicModelling/lda_model.model')
    print(lda_model.print_topics())

    lsa_model = LsiModel(corpus = corpus_of_tokens,
                     id2word = dict_of_tokens,
                     num_topics = 10,
                     decay = 0.5)
    print(lsa_model.print_topics())
    lsa_model.save('TopicModelling/lsa_model.model')
    lda_coherence = CoherenceModel(model = lda_model,
                               corpus = corpus_of_tokens,
                               texts = tokens,
                               dictionary = dict_of_tokens,
                               coherence = 'c_v').get_coherence()

    lsa_coherence = CoherenceModel(model = lsa_model,
                               corpus = corpus_of_tokens,
                               texts = tokens,
                               dictionary = dict_of_tokens,
                               coherence = 'c_v').get_coherence()
