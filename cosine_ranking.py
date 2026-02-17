#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import stopwords
import os
import string
from collections import defaultdict
import copy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


# In[2]:


docdf = pd.read_csv('IRdata_Resource.csv')


# In[3]:


docdf


# In[4]:


docdf.drop([docdf.columns[0]], axis=1, inplace=True)


# In[5]:


docdf.head()


# In[6]:


docdf.shape


# In[7]:


docs = []
doclinks = []

for i in range(docdf.shape[0]):
    doclinks.append(docdf['link'][i])
    docs.append(docdf['text'][i])


# ## Preprocessing

# In[8]:


lemmer = nltk.WordNetLemmatizer()

def lemmatizer(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


# In[9]:


def removePunctuation(tokens):
    return[t for t in tokens if t not in string.punctuation]


# In[10]:


stop_words = set(stopwords.words('english'))


# In[11]:


def preprocess(doc):
    procd = []
    line = doc.lower()
    line = word_tokenize(line)
    line = removePunctuation(line)
    line = lemmatizer(line)
    for word in line:
        if(word not in stop_words):
            procd.append(word)
    return procd


# In[12]:


prodocs = []

for doc in docs:
    procd = preprocess(doc)
    prodocs.append(procd)


# In[13]:


len(prodocs)


# ## TF-IDF

# In[14]:


from collections import Counter

def defaultdnorm():
    return 0.5

def defaultidf():
    return np.log(len(prodocs))


# In[15]:


vocab = set()
for doc in prodocs:
    for word in doc:
        if word not in vocab:
            vocab.add(word)

vocab = list(vocab)


# In[16]:


len(vocab)


# In[17]:


class tfidf:
    def __init__(self):
        self.idf = defaultdict(defaultidf)
        self.tfeq = defaultdict(lambda: defaultdict(int))

    def computetf(self, prodocs):
        for i in range(len(prodocs)):
            doc = prodocs[i]
            countdata = Counter(doc)
            for word in doc:
                count = countdata[word]
                self.tfeq[i][word] = count / len(doc)

    def computeidf(self, prodocs):
        temp = defaultdict(set)
        num = len(prodocs)
        for i in range(len(prodocs)):
            doc = prodocs[i]
            for word in doc:
                temp[word].add(i)

        for word in vocab:
            self.idf[word] = np.log(num / (1 + len(temp[word])))


# In[18]:


obj = tfidf()
obj.computetf(prodocs)
obj.computeidf(prodocs)


# In[ ]:





# ## TF-IDF matrices

# In[19]:


tfidfmat = np.zeros((len(prodocs), len(vocab)))

vindex = dict()
for i in range(len(vocab)):
    vindex[vocab[i]] = i


for i in range(len(prodocs)):
    doc = prodocs[i]
    for word in doc:
        ind = vindex[word]
        idf = obj.idf[word]
        tfidfmat[i][ind] = obj.tfeq[i][word] * idf


# In[20]:


# Query = question that user could not solve

df = pd.read_csv('IRdata2.csv')
query = df['question'][1184]
#query = input('Enter the query: ')
tokens = preprocess(query)
tokens


# In[21]:


query


# ## Cosine similarity

# In[22]:


def genqvec(tokens):
    qvec = np.zeros(len(vocab))

    qobj = tfidf()
    qobj.computetf([tokens])

    for word in tokens:
        if(word in vocab):
            ind = vindex[word]
            idf = obj.idf[word]
            qvec[ind] = qobj.tfeq[0][word] * idf
    
    return qvec


# In[23]:


def cossim(d1, d2):
    num = np.dot(d1, d2)
    denom = np.linalg.norm(d1) * np.linalg.norm(d2)
    cossim = num / denom
    return cossim


# In[24]:


qvec = genqvec(tokens)


# In[ ]:





# In[25]:


cosscores = []

for i in range(len(prodocs)):
    cosscores.append(cossim(qvec, tfidfmat[i]))
    
out = np.array(cosscores).argsort()[-10:][::-1]


#print('The top 10 documents for each scheme using cosine similarity are:\n')
#print('Term Frequency:  ', out)


# In[26]:


linklist = [doclinks[val] for val in out]
#print('Cosine similarity scores:\n')
#print('\n', linklist)
#print(sorted(cosscores, reverse=True)[:5])


# In[ ]:





# In[27]:


out


# In[28]:


df.iloc[out]


# In[ ]:





# In[29]:


np.unique(df['domain'])


# In[30]:


df[df['domain'] == 'Alcohols, Phenols & Ethers']


# In[ ]:





# In[31]:


class documentRetriever:
    def __init__(self):
        self.newdf = None
    
    def retrieve(self, query, k):
        tokens = preprocess(query)
        qvec = genqvec(tokens)
        
        cosscores = []
        for i in range(len(prodocs)):
            cosscores.append(cossim(qvec, tfidfmat[i]))

        out = np.array(cosscores).argsort()[-k:][::-1]
        self.newdf = docdf.iloc[out]


# In[ ]:





# In[33]:


qdf = pd.read_csv('IRdata2.csv').drop(['imageURL'], axis=1)
qdf["QID"] = "CH" + qdf["QID"].map(str)


# In[38]:


q1 = qdf['question'][1566]
q1


# In[ ]:





# In[39]:


dr = documentRetriever()
dr.retrieve(q1, 10)
dr.newdf


# In[ ]:





# In[ ]:




