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
from sklearn.model_selection import StratifiedKFold
from sklearn.utils import shuffle
from sklearn.svm import SVC
from sklearn.metrics import multilabel_confusion_matrix, classification_report, confusion_matrix
import numpy as np
import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()

def ml_reader(my_file):
    with open(my_file, 'r') as lda_dev_score:
        dev_reader = csv.reader(lda_dev_score, delimiter = '\t')
        line_counter = False
        X = []
        Y = []
        for row in dev_reader:
            if line_counter is  False:
                line_counter = True
                continue
            sub_data = []
            for i in range(4,len(row)):
                sub_data.append(row[i])
            X.append(sub_data)
            Y.append([row[2]])
    return X, Y

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
    en_stop.add('crash')
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
    W = nmf.fit_transform(tfidf)
    H = nmf.components_
    
    scores_per_document = nmf.transform(tfidf)
    write_scores = open('General/NMFscores.csv', 'w', newline = '\n')
    score_writer = csv.writer(write_scores, delimiter = '\t')
    headers = ['id', 'time', 'developer', 'short_desc']
    for i in range(topic_number):
        headers.append('topic%d'%i)
    score_writer.writerow(headers)
    with open('General/mozilla_learning_data.csv', 'r') as developer_info:
        dev_reader = csv.reader(developer_info, delimiter ='\t')
        line_counter = 0
        line_counter2 = False
        for row in dev_reader:
            if line_counter2 is False:
                line_counter2 = True
                continue
            to_write_data = [row[0], row[1], row[2], row[3]]
            for i in range(topic_number):
                to_write_data.append(W[line_counter][i])
            score_writer.writerow(to_write_data)
            line_counter += 1
    write_scores.close()

    print("\nTopics in NMF model (generalized Kullback-Leibler divergence):")
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    print_top_words(nmf, tfidf_feature_names, 20)

    #STRATIFIED KFLOD CROSS VALIDATION#
    nmf_x, nmf_y = ml_reader('General/NMFscores.csv')
    nmf_x, nmf_y = shuffle(nmf_x, nmf_y)
    nmf_x_np = np.asarray(nmf_x)
    nmf_y_np = np.asarray(nmf_y)
    skf = StratifiedKFold(n_splits = 10)
    skf.get_n_splits(nmf_x_np, nmf_y_np)

    #SVM FOR NNMF
    general_P = []
    general_R = []
    correct_rate = []
    confusion_matrices = []
    fold_num = 0
    for train, test in skf.split(nmf_x_np, nmf_y_np):
        prob_y = []
        x_train , x_test = nmf_x_np[train], nmf_x_np[test]
        y_train , y_test = nmf_y_np[train], nmf_y_np[test]
        clf = SVC(gamma='scale', probability=True, decision_function_shape='ovo')
        clf.fit(x_train, y_train.reshape(len(y_train),1))
        predicted = clf.predict(x_test)
        mcm = multilabel_confusion_matrix(y_test, predicted)
        P = []
        R = []
        F1 = []
        if len(confusion_matrices) == 0:
            for i in range(len(mcm)):
                confusion_matrices.append([[0,0],[0,0]])
        for i in range(len(mcm)):
            a = mcm[i]
            TP = a[0][0]
            FP = a[0][1]
            FN = a[1][0]
            TN = a[1][1]
            Pi = TP/(TP+FP)
            Ri = TP/(TP+FN)
            P.append(Pi)
            R.append(Ri)
            confusion_matrices[i][0][0] += TP
            confusion_matrices[i][0][1] += FP
            confusion_matrices[i][1][0] += FN
            confusion_matrices[i][1][1] += TN
        general_P.append(sum(P)/len(P))
        general_R.append(sum(R)/len(R))
        if(fold_num == 0):
            lda_svm = open('General/mozilla_nmf_svm_confusion.txt', 'w')
            print((fold_num+1), file = lda_svm)
            print(confusion_matrices, file = lda_svm)
            lda_svm.close()
        else:
            lda_svm = open('General/mozilla_nmf_svm_confusion.txt', 'a')
            print((fold_num+1), file = lda_svm)
            print(confusion_matrices, file = lda_svm)
            lda_svm.close()
        print('fold_no_nmf:', fold_num)
        fold_num +=1
    mozilla_results = open('General/mozilla_nmf_results.txt', 'w')
    precision = np.mean(general_P)
    recall = np.mean(general_R)
    F1 = 2*precision*recall/(precision+recall)
    print('NMF', file = mozilla_results)
    print('Precision is', precision, file = mozilla_results)
    print('Recall is', recall, file = mozilla_results)
    print('F1 score is', F1, file = mozilla_results)
    mozilla_results.close()


