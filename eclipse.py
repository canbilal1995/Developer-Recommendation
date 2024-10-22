#@Author: Bilal CAN

import csv
import os
from gensim.models import LdaModel, LsiModel
from gensim.models.coherencemodel import CoherenceModel
from gensim import corpora
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.model_selection import StratifiedKFold
from sklearn.utils import shuffle
from sklearn.svm import SVC
from sklearn.metrics import multilabel_confusion_matrix, classification_report, confusion_matrix
import numpy as np
import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

def tokenizer(texts):
    tokens = []
    p_stemmer = PorterStemmer()
    tokenizer = RegexpTokenizer(r'\w+')
    en_stop = set(stopwords.words('english')) #stopwords
    en_stop.add('eclipse')
    en_stop.add('error')
    en_stop.add('project')
    for element in range(len(texts)):
        sub_tokens = []
        for word in range(len(texts[element])):
            sub_tokens += tokenizer.tokenize(texts[element][word]) #atomic words are gathered from each word
            stopped_sub_tokens = [i for i in sub_tokens if not i in en_stop] #stopwords are discarded
            stemmed_sub_tokens = [p_stemmer.stem(i) for i in stopped_sub_tokens] #stemming
        tokens += [stemmed_sub_tokens]
    return tokens

def topic_scoring(topics, topic_number):
    score_vector = []
    for topic in topics:
        for index, score in topic:
            while len(score_vector) < index:
                score_vector.append(0)
            score_vector.append(score)
        while len(score_vector) < topic_number:
            score_vector.append(0)
    return score_vector

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

    tokens = tokenizer(texts)

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
    

    #CALCULATING SCORES of EACH JOB DONE BY DEVELOPERS#
    developer_scores = open('General/eclipse_topic_scores_lda.csv', 'w', newline = '\n')
    developer_scores2 = open('General/eclipse_topic_scores_lsa.csv', 'w', newline = '\n')
    score_writer = csv.writer(developer_scores, delimiter = '\t')
    score_writer2 = csv.writer(developer_scores2, delimiter = '\t')
    headers = ['id', 'time', 'developer', 'short_desc']
    for i in range(topic_number):
        headers.append('topic%d'%i)
    score_writer.writerow(headers)
    score_writer2.writerow(headers)
    with open('General/eclipse_learning_data.csv', 'r') as developer_info:
        dev_reader = csv.reader(developer_info, delimiter = '\t')
        line_counter = False
        for row in dev_reader:
            if line_counter is False:
                line_counter = True
                continue
            my_text = [row[3].strip().split()]
            tokenized_text = tokenizer(my_text)
            bow_vector = [dict_of_tokens.doc2bow(doc, allow_update = False) for doc in tokenized_text]
            #score calculation for lda is below.
            topics = lda_model[bow_vector]
            score_vector = topic_scoring(topics, topic_number)
            #score calculation is over.
            #lda data is started to write to the file.
            to_write_data = [row[0], row[1], row[2], row[3]]
            to_write_data.extend(score_vector)
            score_writer.writerow(to_write_data)
            #lda data is written to the file.
            
            #score calculation for lsa is below.
            topics = lsa_model[bow_vector]
            score_vector = topic_scoring(topics, topic_number)
            #score calculation is over.
            #lsa data is started to write to the file.
            to_write_data = [row[0], row[1], row[2], row[3]]
            to_write_data.extend(score_vector)
            score_writer2.writerow(to_write_data)
            #lsa data is written to the file.
    developer_scores.close()
    developer_scores2.close()

    #STRATIFIED K_FOLD CROSS VALIDATION FOR LDA DATA#
    lda_X, lda_Y = ml_reader('General/eclipse_topic_scores_lda.csv')
    lda_X, lda_Y = shuffle(lda_X, lda_Y)
    lda_X_np = np.asarray(lda_X)
    lda_Y_np = np.asarray(lda_Y)
    skf = StratifiedKFold(n_splits = 10)
    skf.get_n_splits(lda_X_np, lda_Y_np)

    #SVM FOR LDA DATA
    #Rrecall = []
    #Pprecision = []
    general_P = []
    general_R = []
    correct_rate = []
    confusion_matrices = []
    fold_num = 0
    for train, test in skf.split(lda_X_np, lda_Y_np):
        prob_y = []   
        x_train, x_test = lda_X_np[train], lda_X_np[test]
        y_train, y_test = lda_Y_np[train], lda_Y_np[test]
        clf = SVC(gamma='scale', probability=True, decision_function_shape='ovo')
        clf.fit(x_train, y_train.reshape(len(y_train),1))
        prob_y.append(clf.predict_proba(x_test))
        correct = 0
        fail = 0
        for my_test in range(len(prob_y[0])):
            prob_dev = []
            for i, p in enumerate(prob_y[0][my_test]):
                prob_dev.append([p, clf.classes_[i]])
            prob_dev.sort(key=lambda a: a[0], reverse=True) #developers in order
            top10 = []
            for i in range(10):
                top10.append(prob_dev[i][1])
            if y_test[my_test] in top10:
                correct += 1
            else:
                fail += 1
        correct_rate.append(correct/(correct+fail))
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
            lda_svm = open('General/eclipse_lda_svm_confusion.txt', 'w')
            print((fold_num+1), file = lda_svm)
            print(confusion_matrices, file = lda_svm)
            lda_svm.close()
        else:
            lda_svm = open('General/eclipse_lda_svm_confusion.txt', 'a')
            print((fold_num+1), file = lda_svm)
            print(confusion_matrices, file = lda_svm)
            lda_svm.close()
        print('fold_no_lda:', fold_num)
        fold_num +=1
    eclipse_results = open('General/eclipse_results.txt', 'w')
    precision = np.mean(general_P)
    recall = np.mean(general_R)
    F1 = 2*precision*recall/(precision+recall)
    print('LDA', file = eclipse_results)
    print('Precision is', precision, file = eclipse_results)
    print('Recall is', recall, file = eclipse_results)
    print('F1 score is', F1, file = eclipse_results)
    eclipse_results.close()


    
    #STRATIFIED K_FOLD CROSS VALIDATION FOR LSA DATA#
    lsa_X, lsa_Y = ml_reader('General/eclipse_topic_scores_lsa.csv')
    lsa_X, lsa_Y = shuffle(lsa_X, lsa_Y)
    lsa_X_np = np.asarray(lsa_X)
    lsa_Y_np = np.asarray(lsa_Y)
    skf = StratifiedKFold(n_splits = 10)
    skf.get_n_splits(lsa_X_np, lsa_Y_np)

    #SVM FOR LSA DATA
    general_P = []
    general_R = []
    correct_rate = []
    confusion_matrices2 = []
    fold_num = 0
    for train, test in skf.split(lsa_X_np, lsa_Y_np):
        prob_y = []   
        x_train, x_test = lsa_X_np[train], lsa_X_np[test]
        y_train, y_test = lsa_Y_np[train], lsa_Y_np[test]
        clf = SVC(gamma='scale', probability=True, decision_function_shape='ovo')
        clf.fit(x_train, y_train.reshape(len(y_train),1))
        prob_y.append(clf.predict_proba(x_test))
        correct = 0
        fail = 0
        for my_test in range(len(prob_y[0])):
            prob_dev = []
            for i, p in enumerate(prob_y[0][my_test]):
                prob_dev.append([p, clf.classes_[i]])
            prob_dev.sort(key=lambda a: a[0], reverse=True) #developers in order
            top10 = []
            for i in range(10):
                top10.append(prob_dev[i][1])
            if y_test[my_test] in top10:
                correct += 1
            else:
                fail += 1
        correct_rate.append(correct/(correct+fail))
        predicted = clf.predict(x_test)
        mcm = multilabel_confusion_matrix(y_test, predicted)
        P = []
        R = []
        F1 = []
        if len(confusion_matrices2) == 0:
            for i in range(len(mcm)):
                confusion_matrices2.append([[0,0],[0,0]])
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
            confusion_matrices2[i][0][0] += TP
            confusion_matrices2[i][0][1] += FP
            confusion_matrices2[i][1][0] += FN
            confusion_matrices2[i][1][1] += TN
        general_P.append(sum(P)/len(P))
        general_R.append(sum(R)/len(R))
        if(fold_num == 0):
            lsa_svm = open('General/eclipse_lsa_svm_confusion.txt', 'w')
            print((fold_num+1), file = lsa_svm)
            print(confusion_matrices2, file = lsa_svm)
            lsa_svm.close()
        else:
            lsa_svm = open('General/eclipse_lsa_svm_confusion.txt', 'a')
            print((fold_num+1), file = lsa_svm)
            print(confusion_matrices2, file = lsa_svm)
            lsa_svm.close()
        print('fold_no_lsa:', fold_num)
        fold_num +=1
    eclipse_results = open('General/eclipse_results.txt', 'a')
    precision = np.mean(general_P)
    recall = np.mean(general_R)
    F1 = 2*precision*recall/(precision+recall)
    print('LSA', file = eclipse_results)
    print('Precision is', precision, file = eclipse_results)
    print('Recall is', recall, file = eclipse_results)
    print('F1 score is', F1, file = eclipse_results)
    eclipse_results.close()
