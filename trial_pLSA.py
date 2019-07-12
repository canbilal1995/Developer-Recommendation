#@Author: Bilal CAN

import csv
import os
from gensim import corpora
from gensim.models.coherencemodel import CoherenceModel
import sklearn
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.preprocessing import normalize
from nltk.corpus import stopwords

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()
    
if __name__ == "__main__":
    topic_number = 10
    loaded_dict = corpora.Dictionary.load('TopicModelling/myDict.dict')
    loaded_corpus = corpora.MmCorpus('TopicModelling/myCorpus.mm')
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
               texts.append(row[3])
    en_stop = set(stopwords.words('english')) #stopwords
    en_stop.add('eclipse')
    en_stop.add('error')
    en_stop.add('project')
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,
                                   max_features=len(loaded_dict),
                                   stop_words=en_stop)
    tfidf = tfidf_vectorizer.fit_transform(texts)
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                max_features=len(loaded_dict),
                                stop_words=en_stop)
    tf = tf_vectorizer.fit_transform(texts)
    nmf = NMF(n_components=topic_number, random_state=1,
          alpha=.1, l1_ratio=.5).fit(tfidf)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    print_top_words(nmf, tfidf_feature_names, 20)
    print("Fitting the NMF model (generalized Kullback-Leibler divergence) with "
      "tf-idf features, n_samples=%d and n_features=%d..."
      % (len(texts), len(loaded_dict)))

    nmf = NMF(n_components=topic_number, random_state=1,
          beta_loss='kullback-leibler', solver='mu', max_iter=1000, alpha=.1,
          l1_ratio=.5).fit(tfidf)

    scores_per_document = nmf.transform(tfidf)
    write_scores = open('General/NMFscores.csv', 'w', newline = '\n')
    score_writer = csv.writer(write_scores, delimiter = '\t')
    headers = ['id', 'time', 'developer', 'short_desc']
    for i in range(topic_number):
        headers.append('topic%d'%i)
    score_writer.writerow(headers)
    with open('General/eclipse_learning_data.csv', 'r') as developer_info:
        dev_reader = csv.reader(developer_info, delimiter ='\t')
        line_counter = 0
        line_counter2 = False
        for row in dev_reader:
            if line_counter2 is False:
                line_counter2 = True
                continue
            to_write_data = [row[0], row[1], row[2], row[3]]
            for i in range(topic_number):
                to_write_data.append(scores_per_document[line_counter][i])
            score_writer.writerow(to_write_data)
            line_counter += 1
    write_scores.close()
    print("\nTopics in NMF model (generalized Kullback-Leibler divergence):")
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    print_top_words(nmf, tfidf_feature_names, 20)
