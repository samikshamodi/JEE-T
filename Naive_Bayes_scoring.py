#!/usr/bin/env python
# coding: utf-8

# In[140]:


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
import sklearn.utils
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')


# In[224]:


def preprocess(dataset, subdomain, domain, links, test):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    data = {}
    sub = {}
    
    for c,i in enumerate(subdomain):
        if test == "train":
            data[i] = []
            sub[i] = [domain[c], links[c]]
        else:
            data[domain[c] + " : " + subdomain[c]] = []
        
    for i, value in enumerate(dataset):
        linetoken = nltk.RegexpTokenizer(r"\w+").tokenize(value)
        linetoken = [i.lower() for i in linetoken]
        linetoken = [word for word in linetoken if not word in stop_words]
        linetoken = [lemmatizer.lemmatize(word) for word in linetoken]
        linetoken = [word for word in linetoken if word.isalnum()]
        if test == "train":
            data[subdomain[i]] += linetoken
        else:
            data[domain[i] + " : " + subdomain[i]] += linetoken
        
    return data, sub


# In[249]:


def dataset(documents, testdata, ratio):
    np.random.seed(0)
    dataset = []
    label = []
    x_test = []
    y_test = []
    for filename, value in documents.items():
        dataset.append(value)
        label.append(filename)
    
    dataset, label = sklearn.utils.shuffle(dataset,label)
    
    for filename, value in testdata.items():
        x_test.append(value)
        y_test.append(filename)
        
    x_test, y_test = sklearn.utils.shuffle(x_test, y_test)
    
    k = int(np.floor(ratio*len(x_test)))
    return dataset, label, x_test[0:k], y_test[0:k]


# In[38]:


def uniqueWords(documents):
    bow = {}
    word_list = {}
    for i, t in enumerate(documents.items()):
        filename = t[0]
        value = t[1]
        bow[filename] = {}
        word_list_word = {}
        for word in value:
            if word not in bow[filename]:
                bow[filename][word] = 1
            else:
                bow[filename][word] += 1

        unique = sorted(list(set(value)))
        for i, word in enumerate(unique):
            word_list_word[word] = i
    
        word_list[filename] = word_list_word

    return word_list, bow


# In[28]:


def label_dict(label):
    lab = {}
    for l in label:
        lab[l] = 1
    return lab


# In[36]:


def TF(word_dict, label):
    class_tf = {}
    for filename, words in word_dict.items():
        if filename in label:
            tf = {}
            tot = 0
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


# In[41]:


def CF(word_list):
    all_words = {}
    icf = {}
    k = 0
    for label, val in word_list.items():
        k += 1
        for word, count in val.items():
            if word not in all_words:
                all_words[word] = [label]
            else:
                if label not in all_words[word]:
                    all_words[word].append(label)

    for word, labels in all_words.items():
        all_words[word] = len(labels)
        icf[word] = np.log10((k/all_words[word]))
        
    return icf


# In[43]:


def TFICF(class_tf, class_icf):
    tf_icf = copy.deepcopy(class_tf)
    for classname, content in tf_icf.items():
        for word, value in content.items():
            tf_icf[classname][word] = class_tf[classname][word]*class_icf[word]
    return tf_icf


# In[53]:


def feature_selection(x1,y1, tf_icf, documents, k = 100):
    c = np.unique(y1)
    sep = {}
    for i in c:
        sep[i] = []
    
    for i in range(len(y1)):
        sep[y1[i]] += x1[i]
    
    for class_name,_ in sep.items():
        unique_words = set(sep[class_name])
        thresh = {}
        for word in unique_words:
            thresh[word] = tf_icf[class_name][word]
        thresh = {key : value for key, value in sorted(thresh.items(), key=lambda item: item[1], reverse = True)}
        set_sep = set(sep[class_name])
        sep[class_name] = [word for word, val in thresh.items()]
        sep[class_name] = sep[class_name][:k]

    return sep


# In[310]:


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
            
    def predict(self, x, sub):
        y_pred = []
        links = []
        result = []
        for doc in x:
            posteriors = [prob for prob in self.class_prob]
            for word in doc:
                for i in range(self.n_class):
                    if word in self.vocab:
                        posteriors[i] *= self.priors[i][word]*1000
                    else:
                        posteriors[i] *= (1/len(self.priors[i]))*1000
                        
            ind = np.argpartition(posteriors, -7)[-7:]
            link = []
            subd = []
            for i in ind:
                link.append(sub[self.item_frequency[int(i)]][1])
                subd.append([self.item_frequency[int(i)], sub[self.item_frequency[int(i)]][0]])
            
            links.append(link)
            result.append(subd)
            
            y_pred.append(self.item_frequency[np.argmax(posteriors)])
        return y_pred, links, result
    
    
    def accuracy(self, y_p, y):
        count = 0
        for i in range(len(y_p)):
            if y_p[i] == y[i]:
                count += 1 
            
        return count/len(y_p)
    
    def getPriors(self):
        return self.priors


# In[311]:


df = pd.read_csv("IRdata_Resource.csv")
# np.unique(df["subdomain"])
df["input"] = df["text"]
df["label"] = df["subdomain"]
data, subdomain = preprocess(df["input"], df["subdomain"],df["domain"],df["link"], "train")
word_list, word_dict = uniqueWords(data)


# In[312]:


df1 = pd.read_csv("ncert data.csv")
test, _ = preprocess(df1["content"], df1["subdomain"],df1["domain"],df1["domain"], "test")
x_train, y_train, x_test, y_test = dataset(data,test,0.3)


# In[313]:


class_tf = TF(word_dict, label_dict(y_train))
class_icf = CF(word_list)
tf_icf = TFICF(class_tf, class_icf)
features = feature_selection(x_train,y_train,tf_icf, data, k = 100)

nb = NaiveBayes()
nb.fit(x_train, y_train, features)


# In[314]:


predict, links, result_subdomain = nb.predict(x_test, subdomain)
# acc = nb.accuracy(predict,y_test)
# print(acc)


# In[ ]:





# In[315]:


y_test[2]


# In[316]:


result_subdomain[2]


# In[ ]:




