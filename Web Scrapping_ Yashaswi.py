#!/usr/bin/env python
# coding: utf-8

# <font size = 6>Importing Libraries 

# In[1]:


import pandas as pd
import numpy as np
import requests
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tokenize import word_tokenize
import string
import csv
from bs4 import BeautifulSoup


# <font size  = 6>Importing Dataset

# In[2]:


df = pd.read_excel('Input.xlsx')
df.head()


# In[3]:


print("Dimensions : ");df.shape


# In[4]:


df.isnull().sum()


# In[92]:


dupe = df[df.duplicated()]
dupe


# <font size = 6>Creating URL List

# In[5]:


y = [uid for uid in df['URL_ID']]
x = [url for url in df['URL']]
x


# <font size = 6>Data Extraction

# <font size  = 5>Creating GET Requests for each URL

# In[6]:


content = []
for url, uid in zip(x,y):
    response = requests.get(url,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
     # Checking if response was successful
    if response.status_code == 200:
        content.append(BeautifulSoup(response.content,'html.parser'))
    else:
        # Handling the error
        print("Failed to request URL:", url, uid)


# <font size = 5>Creating list for all the articles

# In[7]:


art = []
for c in content:
    art.append(c.find('div', attrs = {'class':'td-post-content'}))


# In[8]:


for i in range(len(art)):
    art[i]= art[i].text.replace('\n',' ')


# In[45]:


df = df[~(df['URL_ID'] == 11668.0) & ~(df['URL_ID'] == 17671.4)]


# <font size = 5>Stop Words

# In[10]:


stop = []
audit = 'StopWords_Auditor.txt'
for sw in open(audit, 'r').readlines():
    stop.append(sw.rstrip())

curr = 'StopWords_Currencies.txt'
for sw in open(curr, 'r').readlines():
    stop.append(sw.rstrip())

gen = 'StopWords_Generic.txt'
for sw in open(gen, 'r').readlines():
    stop.append(sw.rstrip())

glong = 'StopWords_GenericLong.txt'
for sw in open(glong, 'r').readlines():
    stop.append(sw.rstrip())

datenum= 'StopWords_DatesandNumbers.txt'
for sw in open(datenum, 'r').readlines():
    stop.append(sw.rstrip())

geo= 'StopWords_Geographic.txt'
for sw in open(geo, 'r').readlines():
    stop.append(sw.rstrip())
    
name= 'StopWords_Names.txt'
for sw in open(name, 'r').readlines():
    stop.append(sw.rstrip())


# <font size = 5>Counting number of sentences in each article

# In[11]:


sen = []
for a in art:
    sen.append(len(sent_tokenize(a)))


# In[12]:


for i in range(len(art)):
    for w in stop:
        art[i]= art[i].replace('?',' ').replace('.',' ').replace(',',' ').replace('!',' ')


# In[15]:


words = []
for a in art:
    words.append(len(word_tokenize(a)))


# <font size  = 5>Positive and Negative Words

# In[17]:


positive = []
negative = []
pos = 'positive-words.txt'
for p in open(pos, 'r').readlines():
    positive.append(p.rstrip())

neg = 'negative-words.txt'
for n in open(neg, 'r').readlines():
    negative.append(n.rstrip())


# In[52]:


pscore = []
for i in range(len(art)):
    x=0
    for word in positive:

        for letter in art[i].lower().split(' '):
            if letter==word:
                x+=1
    pscore.append(x)


# In[53]:


nscore = []
for i in range(len(art)):
    x=0
    for word in negative:
        for letter in art[i].lower().split(' '):
            if letter == word:
                x+=1
    nscore.append(x)


# In[54]:


df['POSITIVE SCORE'] = pscore
df['NEGITIVE SCORE'] = nscore


# In[56]:


df['POLARITY SCORE'] = (df['POSITIVE SCORE']-df['NEGATIVE SCORE'])/ ((df['POSITIVE SCORE'] +df['NEGATIVE SCORE']))


# In[57]:


df['SUBJECTIVITY SCORE'] = (df['POSITIVE SCORE'] + df['NEGATIVE SCORE'])/( (words) + 0.000001)


# In[59]:


df['AVG SENTENCE LENGTH'] = np.array(words)/np.array(sen)


# In[63]:


def syllables(word):

    syll = 0
    for i in range(len(word)):
        if re.match(r"[aeiouy]", word[i]):
            syll += 1
        if i == len(word) - 2 and word[i] == "e" and word[i + 1] == "d":
            syll -= 1
        if i == len(word) - 2 and word[i] == "e" and word[i + 1] == "s":
            syll -= 1
    return syll


# In[64]:


def complex_words(article):
    comp = 0
    for word in article.split():
        if syllables(word) > 2:
            comp += 1
    return comp


# In[65]:


import re
syll = []
comp = []
# Count the syllables and complex words in each article
for a in art:
    syll.append(syllables(a))
    comp.append(complex_words(a))


# In[66]:


df['PERCENTAGE OF COMPLEX WORDS'] = np.array(comp)/np.array(words)


# In[67]:


df['FOG INDEX'] = 0.4 * (df['AVG SENTENCE LENGTH'] + df['PERCENTAGE OF COMPLEX WORDS'])


# In[68]:


df['AVG NUMBER OF WORDS PER SENTENCES'] = df['AVG SENTENCE LENGTH']


# In[69]:


df['COMPLEX WORD COUNT'] = comp


# In[73]:


df['WORD COUNT'] = words


# In[78]:


total_ch= [len(a) for a in art]
df['AVG WORD LENGTH'] = np.array(total_ch)/np.array(words)


# In[81]:


pnouns = []
personal_noun =['I', 'we','my', 'ours','and' 'us', 'We','My', 'Ours','And' 'Us'] 
for a in art:
    ans=0
    for w in a:
        if w in personal_noun:
            ans+=1
    pnouns.append(ans)


# In[82]:


df['PERSONAL PRONOUN'] = pnouns


# In[83]:


df


# In[93]:


df.to_csv("SOLUTION.csv")


# In[ ]:




