# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 20:09:03 2018

@author: lihan
"""
import goslate
import pandas as pd
import concurrent.futures
df=pd.read_csv("train_data.csv")
df.ix[:,4].value_counts()
cities=["Edinburgh","Karlsruhe","Montreal","Waterloo","Pittsburgh","Charlotte","Urbana-Champaign","Phoenix","Las Vegas","Madison","Cleveland"]
colnames=df.columns.values.tolist()
new_data=pd.DataFrame(columns=[colnames])
for i in cities:
    new_data=pd.concat([new_data,df[df["city"]==i]],axis=1)

df["stars"][df["text"].str.contains("decilious")].count()
df["stars"][df["text"].str.contains("minutes")].mean()
df["stars"][df["text"].str.contains("minutes")].hist()
df["text"][df["stars"]==1].str.len().mean()
df["text"].to_csv(r'C:\Users\lihan\OneDrive - UW-Madison\window\STAT 628\Module_2\reviews.txt')

with open('reviews.txt', 'rb') as f:
    novel_text = f.read()
gs = goslate.Goslate()
translated_lines = gs.translate(novel_text,"en")
translation = '\n'.join(translated_lines)

from rake_nltk import Rake
import nltk
import string
stopset = set(nltk.corpus.stopwords.words('english'))
stopset.add("us")
stopset.add("would")
stopset.add("go")
stopset.add("get")
stopset.add("also")
stopset.add("got")
stopset.add("every")

r = Rake(stopset,string.punctuation+"?")
all_keywords = list()
all_keywords_split = list()
for i in range(10000):
    r.extract_keywords_from_text(df["text"][i])
    phrases = r.get_ranked_phrases()
    scores = r.get_ranked_phrases_with_scores()
    all_keywords.append([phrases[i] for i in range(len(phrases)) if scores[i][0]>1])
    all_keywords_split.append([nltk.word_tokenize(phrases[i]) for i in range(len(phrases)) if scores[i][0]>1])

import collections

all_keywords_each = list()
for  i in all_keywords_split:
    for j in i:
        for l in range(len(j)):
            all_keywords_each.append(j[l])
            
collections.Counter(all_keywords_each).most_common()[0:99]

emotion_words = pd.read_csv("vader_lexicon.txt",sep = "\t",header=None)

emotion_words_list = emotion_words[0].tolist()
emotion_scores_list = emotion_words[1].tolist()

emotion_words_times = [all_keywords_each.count(i) for i in emotion_words_list]
emotion_words_selected = [emotion_words_list[i] for i in range(len(emotion_words_list)) if emotion_words_times[i]>0]