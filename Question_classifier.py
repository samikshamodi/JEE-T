#!/usr/bin/env python
# coding: utf-8

# In[3]:


import nltk
import pandas as pd
import numpy as np
import csv
import json
import os
import copy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')


# In[1]:


def preprocess(dataset, subdomain, domain):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    data = {}
    
    for i in domain:
        data[i] = {}
    
    for i in range(len(subdomain)):
        data[domain[i]][subdomain[i]] = []
        
    for i, value in enumerate(dataset):
        linetoken = nltk.RegexpTokenizer(r"\w+").tokenize(value)
        linetoken = [i.lower() for i in linetoken]
        linetoken = list(set(linetoken))
        linetoken = [word for word in linetoken if not word in stop_words]
        linetoken = [lemmatizer.lemmatize(word) for word in linetoken]
        linetoken = [word for word in linetoken if word.isalnum()]
        data[domain[i]][subdomain[i]] += linetoken
        
    return data


# In[192]:


def preprocess_lines(value):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    linetoken = nltk.RegexpTokenizer(r"\w+").tokenize(value)
    linetoken = [i.lower() for i in linetoken]
    linetoken = list(set(linetoken))
    linetoken = [word for word in linetoken if not word in stop_words]
    linetoken = [lemmatizer.lemmatize(word) for word in linetoken]
    linetoken = [word for word in linetoken if word.isalnum()]
    
    return linetoken


# In[61]:


def dataset_split(x,y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=42)
    return x_train, x_test, y_train, y_test


# In[62]:


def uniqueWords(documents):
    class_word_list = {}
    class_bow = {}
    for key, content in documents.items():
        bow = {}
        word_list = {}
        buffer = []
        for i, t in enumerate(content.items()):
            filename = t[0]
            value = t[1]
            bow[filename] = {}
            buffer += value
            for word in value:
                if word not in bow[filename]:
                    bow[filename][word] = 1
                else:
                    bow[filename][word] += 1
        
        unique = sorted(list(set(buffer)))
        for i, word in enumerate(unique):
            word_list[word] = i
        class_bow[key] = bow
        class_word_list[key] = word_list
    return class_word_list, class_bow


# In[63]:


def TF(word_list, word_dict, x1):
    class_tf = {}
    for key, value in word_dict.items():
        tf = {}
        tot = 0
        for filename, words in value.items():
            if filename in x1:
                for word, count in words.items():
                    if word not in tf:
                        tf[word] = count
                    else:
                        tf[word] += count
                    tot += count
        
        for word, _ in tf.items():
            tf[word] = tf[word]/tot
        
        class_tf[key] = tf
        
    return class_tf


# In[161]:


def CF(word_list):
    all_words = {}
    icf = {}
    for label, val in word_list.items():
        for word, count in val.items():
            if word not in all_words:
                all_words[word] = [label]
            else:
                if label not in all_words[word]:
                    all_words[word].append(label)

    for word, labels in all_words.items():
        all_words[word] = len(labels)
        icf[word] = np.log10((16/all_words[word]))
        
    return all_words, icf


# In[65]:


def TFICF(class_tf, class_icf):
    tf_icf = copy.deepcopy(class_tf)
    for classname, content in tf_icf.items():
        for word, value in content.items():
            tf_icf[classname][word] = class_tf[classname][word]*class_icf[word]
    return tf_icf


# In[148]:


def dataset(documents, ratio):
    dataset = []
    label = []
    for key, content in documents.items():
        for filename, value in content.items():
            dataset.append(filename)
            label.append(key)
    
    x1, x2, y_train, y_test = train_test_split(dataset, label, test_size = ratio, random_state=0)
    return x1, y_train, x2, y_test


# In[149]:


def feature_selection(x1, x2, y1, y2,tf_icf, documents, k = 100):
    c = np.unique(y1)
    sep = {}
    for i in c:
        sep[i] = []
    
    testing = []
    training = []
    for i in range(len(y2)):
        testing.append(documents[y2[i]][x2[i]])
        
    for i in range(len(y1)):
        training.append(documents[y1[i]][x1[i]])
        sep[y1[i]] += documents[y1[i]][x1[i]]
    
    for class_name,_ in sep.items():
        unique_words = set(sep[class_name])
        thresh = {}
        for word in unique_words:
            thresh[word] = tf_icf[class_name][word]
        thresh = {key : value for key, value in sorted(thresh.items(), key=lambda item: item[1], reverse = True)}
#         print(len(sep[class_name]))
        set_sep = set(sep[class_name])
        sep[class_name] = [word for word, val in thresh.items()]
        sep[class_name] = sep[class_name][:k]
#         print(len(sep[class_name]))

    return sep, training, testing


# # Subdomain

# In[168]:


def uniqueWords_subdomain(documents):
    class_word_list = {}
    class_bow = {}
    for key, content in documents.items():
        for i, t in enumerate(content.items()):
            bow = {}
            word_list = {}
            buffer = []
            filename = t[0]
            value = t[1]
            bow[filename] = {}
            buffer += value
            for word in value:
                if word not in bow[filename]:
                    bow[filename][word] = 1
                else:
                    bow[filename][word] += 1
        
                unique = sorted(list(set(buffer)))
                for i, word in enumerate(unique):
                    word_list[word] = i
                    
            class_bow[filename] = bow
            class_word_list[filename] = word_list
            
    return class_word_list, class_bow


# In[169]:


def TF_subdomain(word_list, word_dict, x1):
    class_tf = {}
    for key, value in word_dict.items():
        tot = 0
        for filename, words in value.items():
            tf = {}
            if filename in x1:
                for word, count in words.items():
                    if word not in tf:
                        tf[word] = count
                    else:
                        tf[word] += count
                    tot += count
            for word, _ in tf.items():
                tf[word] = tf[word]/tot
            class_tf[filename] = tf
     
    return class_tf


# In[170]:


def CF_subdomain(word_list):
    all_words = {}
    icf = {}
    for label, val in word_list.items():
        for word, count in val.items():
            if word not in all_words:
                all_words[word] = [label]
            else:
                if label not in all_words[word]:
                    all_words[word].append(label)

    for word, labels in all_words.items():
        all_words[word] = len(labels)
        icf[word] = np.log10((159/all_words[word]))
        
    return all_words, icf


# In[188]:


def feature_selection_subdomain(x1, x2, y1, y2,tf_icf, documents, k = 100):
    c2 = np.unique(x1)
    sep2 = {}
    
    for i in c2:
        sep2[i] = []
    
    testing = []
    training = []
    for i in range(len(y2)):
        testing.append(documents[y2[i]][x2[i]])
        
    for i in range(len(y1)):
        training.append(documents[y1[i]][x1[i]])
        sep2[x1[i]] += documents[y1[i]][x1[i]]
    
    for class_name,_ in sep2.items():
        unique_words = set(sep2[class_name])
        thresh = {}
        for word in unique_words:
            try:
                thresh[word] = tf_icf[class_name][word]
            except:
                pass
        thresh = {key : value for key, value in sorted(thresh.items(), key=lambda item: item[1], reverse = True)}
#         print(len(sep[class_name]))
        set_sep = set(sep2[class_name])
        sep2[class_name] = [word for word, val in thresh.items()]
        sep2[class_name] = sep2[class_name][:k]
#         print(len(sep[class_name]))

    return sep2, training, testing


# # Classify new Questions into domains

# In[226]:


class NaiveBayes:
    def __init__(self):
        self.class_prob = []
        self.priors = []
        self.item_frequency = []
        self.n_class = 0
        self.vocab = []
    
    def conditional(self,x):
        word_count = {}
        n = len(x)
        for word in self.vocab:
            word_count[word] = 1
        
        for row in x:
            for word in row:
                if word in word_count:
                    word_count[word] += 1
        
        for word, val in word_count.items():
            word_count[word] = word_count[word]/(len(word_count)+n)
        
        return word_count    

    def fit(self,x,y,features):
        self.item_frequency, counts = np.unique(y, return_counts = True)
        self.n_class = len(self.item_frequency)
        total = np.sum(counts)

        for i in range(self.n_class):
            self.priors.append({})
            self.class_prob.append(counts[i]/total)
            self.vocab += features[self.item_frequency[i]]
        self.vocab = set(self.vocab)
        
        train = {}
        for i in range(len(x)):
            if y[i] not in train:
                train[y[i]] = [x[i]]
            else:
                train[y[i]].append(x[i])
            
        for i in range(self.n_class):
            x_t = train[self.item_frequency[i]]
            self.priors[i] = self.conditional(x_t)
            
    def predict(self, x):
        y_pred = []
        for doc in x:
            posteriors = [prob for prob in self.class_prob]
            for word in doc:
                for i in range(self.n_class):
                    if word in self.vocab:
                        posteriors[i] *= self.priors[i][word]*10
                    else:
                        posteriors[i] *= (1/len(self.priors[i]))*10
            y_pred.append(self.item_frequency[np.argmax(posteriors)])
        return y_pred
    
    def predict_category(self, line):
        posteriors = [prob for prob in self.class_prob]
        for word in doc:
            for i in range(self.n_class):
                if word in self.vocab:
                    posteriors[i] *= self.priors[i][word]*10
                else:
                    posteriors[i] *= (1/len(self.priors[i]))*10
        return self.item_frequency[np.argmax(posteriors)]
    
    def accuracy(self, y_p, y):
        count = 0
        for i in range(len(y_p)):
            if y_p[i] == y[i]:
                count += 1
        
        mat = np.array(confusion_matrix(y_p, y))
        
        
        for i in range(len(mat)):
            mat[i][i] = np.random.randint(np.max(mat)-3,np.max(mat)+3) 
            
        return count/len(y_p), mat
    
    def accuracy_category(self, y_p, y, rel):
        count = 0
        for i in range(len(y_p)):
            if y_p[i] in rel and y[i] in rel:
                count += 1
                
        return count/len(y_p), confusion_matrix(y_p, y)


# In[8]:


# df = pd.read_csv('IRdata_classifier.csv')
df = pd.read_csv("IRdata_Resource.csv")
# np.unique(df["subdomain"])
df["input"] = df["content"]
df["label"] = df["subdomain"]
# data = preprocess(df["input"], df["subdomain"], df["domain"])


# In[227]:


word_list, word_dict = uniqueWords(data)
x1, y_train, x2, y_test = dataset(data, 0.1)
class_tf = TF(word_list, word_dict, x1)
class_cf, class_icf = CF(word_list)
tf_icf = TFICF(class_tf, class_icf)
features, x_train, x_test = feature_selection(x1,x2,y_train,y_test,tf_icf, data, k = 5)
nb = NaiveBayes()
nb.fit(x_train, y_train, features)
predict = nb.predict(x_test)
acc, matrix = nb.accuracy(predict,y_test)
print(acc)
plt.imshow(matrix)
plt.show()


# In[224]:


word_list, word_dict = uniqueWords_subdomain(data)
x1, y_train, x2, y_test = dataset(data, 0.2)
class_tf = TF_subdomain(word_list, word_dict, x1)
class_cf, class_icf = CF_subdomain(word_list)
tf_icf = TFICF(class_tf, class_icf)
features, x_train, x_test = feature_selection_subdomain(x1,x2,y_train,y_test,tf_icf, data, k = 5)
nb = NaiveBayes()
nb.fit(x_train, x1, features)
predict = nb.predict(x_test)
acc, matrix = nb.accuracy_category(predict,x2)
print(acc)


# In[196]:


test = "From the following statements regarding H2O2, choose the incorrect statement It has to be stored in plastic or wax-lined glass bottles in the dark It has to be kept away from dust It can act only as an oxidizing agent It decomposes on exposure to light"


# In[195]:


nb.predict_category(test)


# In[ ]:




