#!/usr/bin/env python
# coding: utf-8

# In[2]:


import nltk
import pandas as pd
import numpy as np
import csv
import json


# In[6]:


class Question:
    data = {}
    status = {}
    testpaper = []
    difficulty = {}
    bag = {}
    done = {}
    t_chem = 0
    t_practice = 30

    
    def __init__(self):
        df = pd.read_csv('IRdata2.csv').drop(['imageURL'], axis=1)
        df["QID"] = "CH" + df["QID"].map(str) 
        self.t_chem = len(df)
        self.structure(df)
        self._init_difficulty()
        
    def _init_difficulty(self):
        np.random.seed(0)
        subdomain = self.subtopics()
        q = [len(subdomain)//3, len(subdomain)//3, len(subdomain)//3]
        np.random.shuffle(subdomain)
        self.difficulty["easy"] = subdomain[0:q[0]]
        self.difficulty["medium"] = subdomain[q[0]:q[1]+q[0]]
        self.difficulty["hard"] = subdomain[q[1]+q[0]:q[1]+q[0]+q[2]]

    def structure(self, df):  
        for domain in df["domain"].unique():
            self.data[domain] = {}
            self.bag[domain] = {}
            self.done[domain] = {}
        
        for i in range(len(df)):
            domain = df.loc[i]["domain"]
            subdomain = df.loc[i]["subdomain"]
            self.data[domain][subdomain] = []
            self.bag[domain][subdomain] = {}
            self.done[domain][subdomain] = {}
        
        for i in range(len(df)):
            domain = df.loc[i]["domain"]
            subdomain = df.loc[i]["subdomain"]
            
            qid = df.loc[i]["QID"]
            question = df.loc[i]["question"]
            options = df.loc[i]["options"].strip("][").split(', ')
            
            for i in range(len(options)):
                options[i] = options[i].replace("'", "")
                
            answer = df.loc[i]["answer"]
            exp = df.loc[i]["explaination"]
            
            qdict = {"ID":qid, "question":question, "options": options, "answer": answer, "explanation":exp}
            
            self.data[domain][subdomain].append(qdict)
            self.status[qid] = 0
            self.bag[domain][subdomain][qid] = 1
    
    def subtopics(self):
        g = []
        for domain, subdomains in self.data.items():
            for subdomain, content in subdomains.items():
                g.append([domain,subdomain])
        return g
    
    def _scoring(self,l,level):
        if level == "easy":
            easy = np.floor(self.t_practice*(l[0]+l[1])/(2*(np.sum(l))))
            medium = np.floor(self.t_practice*(l[0]+l[2])/(2*(np.sum(l))))
            hard = self.t_practice - easy - medium
            
        elif level == "medium":
            medium = np.floor(self.t_practice*(l[0]+l[1])/(2*(np.sum(l))))
            easy = np.floor(self.t_practice*(l[0]+l[2])/(2*(np.sum(l))))
            hard = self.t_practice - medium - easy
        
        elif level == "hard":
            hard = np.floor(self.t_practice*(l[0]+l[1])/(2*(np.sum(l))))
            medium = np.floor(self.t_practice*(l[0]+l[2])/(2*(np.sum(l))))
            easy = self.t_practice - medium - hard
            
        return {"easy" : np.int64(easy), "medium" : np.int64(medium), "hard" : np.int64(hard)}
    
    def _check(self, level, questions, domain, subdomain):
        counter = 0
        for i in range(len(questions)):
#             print(questions)
            if questions[i]["ID"] in self.done:
                counter += 1
        
        if counter < len(questions):
            return questions, domain, subdomain
        else:
            k = np.random.randint(0, len(self.difficulty[level]))
            domain = self.difficulty[level][k][0]
            subdomain = self.difficulty[level][k][1]
            q_temp = self.data[domain][subdomain]
            return self._check(level, q_temp, domain, subdomain)
    
    def practice_paper(self, level, n_questions = 30):
        self.t_practice = n_questions
        np.random.seed(0)
        topic_length = sorted([len(self.difficulty["easy"]), len(self.difficulty["medium"]), len(self.difficulty["hard"])])[::-1]
        topic_diff = self._scoring(topic_length,level)
        paper = []
        for key, counter in topic_diff.items():
            for _ in range(counter):
                k = np.random.randint(0,len(self.difficulty[key]))
                domain = self.difficulty[key][k][0]
                subdomain = self.difficulty[key][k][1]
                q_temp = self.data[domain][subdomain]
                q_size = len(self.bag[domain][subdomain])
                if q_size == 0:
                    self.bag[domain][subdomain] = self.done[domain][subdomain]
                    del self.done[domain][subdomain]
                    self.done[domain][subdomain] = {}
                    q_size = len(self.bag[domain][subdomain])

                element = np.random.randint(0, q_size)
                id_ = list(self.bag[domain][subdomain])[element]
                question = {}
                for i in range(len(self.data[domain][subdomain])):
                    if self.data[domain][subdomain][i]["ID"] == id_:
                        selection = self.data[domain][subdomain][i]
                        break
                selection[domain] = domain
                selection[subdomain] = subdomain
                self.done[domain][subdomain][id_] = 0
                del self.bag[domain][subdomain][id_]
                paper.append(selection)
#                 selection = q_temp[element]
                
#                     if selection["ID"] not in self.done:
#                         self.done[selection["ID"]] = 0
#                         selection["domain"] = domain
#                         selection["subdomain"] = subdomain
#                         paper.append(selection)
#                         break

#                 q_temp, domain, subdomain = self._check(key, q_temp, domain, subdomain)
#                 q_size = len(q_temp)
#                 while True:
#                     element = np.random.randint(0, q_size)
#                     selection = q_temp[element]
#                     if selection["ID"] not in self.done:
#                         self.done[selection["ID"]] = 0
#                         selection["domain"] = domain
#                         selection["subdomain"] = subdomain
#                         paper.append(selection)
#                         break
        np.random.shuffle(paper)
        return paper
    
    def setDifficulty(self, cat):
        self.difficulty = cat
            
    def getData(self):
        return self.data
    
    def getDoneQuestions(self):
        return self.done


# In[1]:
def make_paper(difficulty,nQ,file):

    f = open("userData/jsons/"+file+".json")
    data = json.load(f)
    dataset.setDifficulty(data)
    paper2 = dataset.practice_paper(difficulty,nQ)
    return paper2

dataset = Question()
diagonistic = dataset.practice_paper("easy")


# In[9]:


# f = open('new.json')
# data = json.load(f)
# dataset.setDifficulty(data)
# paper2 = dataset.practice_paper("medium")


# In[10]:


diagonistic = dataset.practice_paper("easy")


# In[11]:


data = dataset.getData()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




