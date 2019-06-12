#@Author: Bilal CAN

import os
from gensim import corpora
from gensim.models.coherencemodel import CoherenceModel
import sklearn
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer;
from sklearn.decomposition import NMF;
from sklearn.preprocessing import normalize;

if __name__ == "__main__":
    loaded_dict = corpora.Dictionary.load('TopicModelling/myDict.dict')
    loaded_corpus = corpora.MmCorpus('TopicModelling/myCorpus.mm')
