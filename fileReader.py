#!/usr/bin/env python
# coding: utf-8

# In[32]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from io import StringIO
from datetime import datetime
import fileReader as fr


# In[ ]:





# In[4]:


def readFile(filename):
    file = open(filename)
    temp = file.read()
    testlist = temp.split('END\nEND')
    # Removing last entry that is blank
    testlist.pop()

    cols = ['time', 'qid', 'domain', 'subdomain', 'qtext', 'correct', 'chosen']
    colstring = ''
    for i in cols:
        colstring += i + ','
    colstring += '\n'
    
    
    for i in range(len(testlist)):
        data = testlist[i]
        dfstring = colstring + data
        dfdata = StringIO(dfstring)
        df = pd.DataFrame()
        df = pd.read_csv(dfdata, sep=',')
        df = df.drop(df.columns[-1], axis=1)
        st = df['time'][0]
        df.drop(0, inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        # preprocess each test df
        testlist[i] = preprocess(df, st)
    
    last5data = pd.concat(testlist[-5:])
    last5data.reset_index(drop=True, inplace=True)
    fulldata = pd.concat(testlist)
    fulldata.reset_index(drop=True, inplace=True)
    
    return fulldata, last5data


# In[5]:


def getTime(dt1, dt2):
    # dt2 > dt1
    diff = dt2 - dt1
    time = diff.seconds
    time += diff.microseconds / 10**6
    return time


# In[6]:


def preprocess(df, st):
    st = st.split(',')[0]
    startdt = datetime.fromisoformat(st)
    
    for i in range(df.shape[0]):
        text = df.iloc[i][0]
        dtobj = datetime.fromisoformat(text)
        df.iloc[i][0] = dtobj
    
    times = []
    dts = [startdt] + list(df['time'])
    
    # Multiply by k to bring times near to real world values
    k = 2

    for i in range(df.shape[0]):
        df.iloc[i][0] = getTime(dts[i], dts[i+1]) * k
    
    acc = []
    for i in range(df.shape[0]):
        if(df.loc[i]['correct'] == df.iloc[i]['chosen']):
            acc.append(1)
        else:
            acc.append(0)
    df['accuracy'] = acc
    
    diff = np.zeros(len(df))
    for i in range(len(df)):
        time = df['time'][i]
        acc = df['accuracy'][i]
        score = np.log(1 + time)
        if(acc == 1):
            score *= 0.75
        else:
            score *= 1.5
        diff[i] = score
    df['difficulty'] = diff
    
    return df


# In[7]:


def handle(scores, em, mh):
    diff = mh - em
    l = em - 0
    r = len(scores) - mh
    if(diff == 0):
        if(l >= r):
            if(r == 0):
                em -= 3
            else:
                em -= 2
                mh += 1
        else:
            if(l == 0):
                mh += 3
            else:
                mh += 2
                em -= 1

    elif(diff == 1):
        if(l == 0):
            mh += 2
        elif(r == 0):
            em -= 2
        else:
            em -= 1
            mh += 1

    elif(diff == 2):
        if(l > r):
            em -= 1
        else:
            mh += 1
    return em, mh


# In[8]:


def classify(df):
    sddict = dict()
    for i in range(df.shape[0]):
        sddict[df['subdomain'][i]] = df['domain'][i]
    
    domaindf = df.groupby('subdomain').mean()
    
    # For chemistry score for time <45 means easy, and between 45 and 90 is intermediate
    ezt = 2
    medt = 4
    ezth = np.log(1+ezt) * 0.75
    medth = np.log(1+medt) * 0.75
    
    scores = sorted(zip(domaindf['difficulty'], domaindf.index))
    
    k = 3
    ez = scores[:k]
    med = []
    hard = scores[-k:]
    scoresmid = scores[k:-k]
    
    emidx = 0
    mhidx = 0
    for i in range(len(scoresmid)):
        val = scoresmid[i]
        if(val[0] < ezth):
            emidx += 1
            mhidx += 1
        elif(val[0] < medth):
            mhidx += 1
    
    if((mhidx - emidx) < k):
        emidx, mhidx = handle(scoresmid, emidx, mhidx)
    
    for i in range(len(scoresmid)):
        entry = scoresmid[i]
        if(i < emidx):
            ez.append(entry)
        elif(i<mhidx):
            med.append(entry)
        else:
            hard.append(entry)
    
    tdict = {}
    for e in ez:
        tdict[e[1]] = 'easy'
    for e in med:
        tdict[e[1]] = 'medium'
    for e in hard:
        tdict[e[1]] = 'hard'
    
    tiers = []
    for sd in domaindf.index:
        tiers.append(tdict[sd])
    
    domaindf['tier'] = tiers
    
    ret = dict()
    ret['easy'] = []
    ret['medium'] = []
    ret['hard'] = []
    
    for sd in domaindf.index:
        ll = []
        ll.append(sddict[sd])
        ll.append(sd)
        ret[domaindf.loc[sd]['tier']].append(ll)
    
    return ret


# In[ ]:





# ### Classification with avg values

# In[43]:


def scorer(val):
    return np.log(1 + val) * 0.75


# In[44]:


def classify2(df):
    sddict = dict()
    for i in range(df.shape[0]):
        sddict[df['subdomain'][i]] = df['domain'][i]
    
    domaindf = df.groupby('subdomain').mean()
    sampledf = pd.read_csv('userData/sampleData.csv')
    grouped = sampledf.groupby('subdomain').mean()
    
    # Score below 80% of average will be easy, above 120% of average will be hard
    m1 = 0.8
    m2 = 1.2
    ezt = dict()
    medt = dict()
    for sd in grouped.index:
        ezt[sd] = m1 * grouped['average'][sd]
        medt[sd] = m2 * grouped['average'][sd]

    
    cmul = 0.75
    wmul = 1.5
    
    scores = sorted(zip(domaindf['difficulty'], domaindf.index))
    
    k = 3
    ez = scores[:k]
    med = []
    hard = scores[-k:]
    scoresmid = scores[k:-k]
    
    emidx = 0
    mhidx = 0
    for i in range(len(scoresmid)):
        val = scoresmid[i]
        if(val[0] < scorer(ezt[val[1]])):
            emidx += 1
            mhidx += 1
        elif(val[0] < scorer(medt[val[1]])):
            mhidx += 1
    
    if((mhidx - emidx) < k):
        emidx, mhidx = handle(scoresmid, emidx, mhidx)
    
    for i in range(len(scoresmid)):
        entry = scoresmid[i]
        if(i < emidx):
            ez.append(entry)
        elif(i<mhidx):
            med.append(entry)
        else:
            hard.append(entry)
    
    tdict = {}
    for e in ez:
        tdict[e[1]] = 'easy'
    for e in med:
        tdict[e[1]] = 'medium'
    for e in hard:
        tdict[e[1]] = 'hard'
    
    tiers = []
    for sd in domaindf.index:
        tiers.append(tdict[sd])
    
    domaindf['tier'] = tiers
    
    ret = dict()
    ret['easy'] = []
    ret['medium'] = []
    ret['hard'] = []
    
    for sd in domaindf.index:
        ll = []
        ll.append(sddict[sd])
        ll.append(sd)
        ret[domaindf.loc[sd]['tier']].append(ll)
    
    return ret


# In[ ]:





# In[ ]:





# In[45]:


class reader:
    def __init__(self):
        self.filename = ''
        self.fulldf = None
        self.l5df = None
        self.diffdict = dict()
    
    def read(self, path):
        self.filename = path
        self.fulldf, self.l5df = readFile(self.filename)
        self.diffdict = classify2(self.l5df)


# In[ ]:





# In[40]:


path = 'userData/csvs/arsed.csv'


# In[46]:


read2 = reader()


# In[47]:


read2.read(path)


# In[48]:


read2.diffdict


# In[49]:


(read2.fulldf['accuracy'] == 1)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




