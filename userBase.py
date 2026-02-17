#!/usr/bin/env python
# coding: utf-8

# In[41]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from io import StringIO
from datetime import datetime
import os
import json
import fileReader as fr


# ## Updating Userbase

# In[40]:


cols = ['username', 'total_attempted', 'total_correct', 'strong_areas', 'weak_areas', 'last_5_papers_accuracy']


# In[ ]:





# In[39]:


def assess(correct, counts):
    strong = []
    weak = []
    lowth = 0.3
    highth = 0.7
    
    for domain in correct.index:
        val = correct[domain] / counts[domain]
        if(val < lowth):
            weak.append(domain)
        elif(val > highth):
            strong.append(domain)
    
    return strong, weak


# In[32]:


# working on it

def update(udf, row):
    cols = udf.columns
    newdf = pd.DataFrame(columns=cols)

    for i in range(udf.shape[0]):
        if(row.iloc[0]['username'] == udf.loc[i]['username']):
            rowdict = row.iloc[0].to_dict()
            udf.drop(udf[udf.username == row.iloc[0]['username']].index, inplace=True)
    newdf = pd.concat([udf, row])
    return newdf


# In[33]:


qdf.iloc[0].to_dict()


# In[34]:


qdf.iloc[9]


# In[35]:


def process(rr):
    full = rr.fulldf
    l5 = rr.l5df
    file = rr.filename
    name = file.split('.')[0]
    name = name.split('/')[-1]
    tq = full.shape[0]
    tc = sum(full['correct'] == full['chosen'])
    tq5 = l5.shape[0]
    true = (l5['correct'] == l5['chosen'])
    tc5 = sum(true)
    acc5 = tc5 / tq5
    l5['true'] = true
    dcorrect = l5.groupby('domain').sum()['true']
    dcounts = l5.groupby('domain').count()['correct']
    strong, weak = assess(dcorrect, dcounts)
    temp = pd.DataFrame([[name, tq, tc, strong, weak, acc5]], columns = cols)
    
    if os.path.exists('userData/users/users.csv'):
        udf = pd.read_csv('userData/users/users.csv')
    else:
        udf = pd.DataFrame(columns = cols)
        udf.to_csv('userData/users/users.csv', index=False)
    
    udf = update(udf, temp)
    udf.to_csv('userData/users/users.csv', index=False)
    return temp


# In[ ]:





# In[46]:


def readFiles():
    for filename in os.listdir('userData/csvs'):
        try:
            rr = fr.reader()
            rr.read('userData/csvs/' + filename)
            process(rr)
            name = filename.split('.')[0]
            with open('userData/jsons/' + name + '.json', 'w') as outfile:
                json.dump(rr.diffdict, outfile)
            print('File read:', filename)
        except:
            print('File not read:', filename)


# In[ ]:





# In[50]:


readFiles()


# In[ ]:





# In[51]:


t2 = pd.read_csv('userData/users/users.csv')
t2


# In[ ]:





# In[ ]:





# # Simulating user data (ignore)

# In[5]:


qdf = pd.read_csv('IRdata2.csv').drop(['imageURL'], axis=1)
qdf["QID"] = "CH" + qdf["QID"].map(str)


# In[19]:


qdf


# In[ ]:





# In[83]:


fdata = np.zeros((qdf.shape[0], 12))
fcols = ['qid', 'subdomain', 'u1time', 'u2time', 'u3time', 'u4time', 'u5time',
         'u6time', 'u7time', 'u8time', 'u9time', 'u10time']


# In[84]:


fdf = pd.DataFrame(fdata, columns = fcols)


# In[85]:


fdf['qid'] = qdf['QID']
fdf['subdomain'] = qdf['subdomain']


# In[86]:


fdf


# In[87]:


rtimes = []

for i in range(fdf.shape[0]):
    ll = np.random.uniform(30, 90, size = (fdf.shape[0]))
    rtimes.append(ll)


# In[88]:


rtimes[0]


# In[89]:


for i in range(1, 11):
    col = 'u' + str(i) + 'time'
    fdf[col] = rtimes[i]


# In[91]:


fdf


# In[107]:


means = fdf[fdf.columns[2:]].mean(axis=1)


# In[108]:


fdf['average'] = means


# In[109]:


fdf


# In[97]:


fdf.to_csv('userData/sampleData.csv', index=False)


# In[98]:


fdf.describe()


# In[102]:


grouped = fdf.groupby('subdomain').mean()


# In[111]:


grouped.describe()


# In[106]:


grouped.describe()['average']


# In[ ]:





# In[ ]:





# In[ ]:





# In[3]:


import cosine_ranking as cr


# In[ ]:





# In[6]:


np.unique(qdf['domain'])


# In[7]:


qdf[qdf['domain'] == 'Biomolecules']


# In[14]:


q1 = qdf['question'][1166]
q1


# In[15]:


dr = cr.documentRetriever()
dr.retrieve(q1, 5)
dr.newdf


# In[18]:


print(np.unique(cdf['domain']))
cdf[cdf['domain'] == 'Alcohols, Phenols & Ethers']


# In[27]:


cdf = pd.read_csv('classified.csv')
q2 = cdf['content'][107]


# In[28]:


q2


# In[30]:


dr = cr.documentRetriever()
dr.retrieve(q2, 10)
dr.newdf


# In[ ]:





# In[ ]:





# In[ ]:




