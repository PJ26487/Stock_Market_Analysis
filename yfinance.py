# importing all the libraries 
import pandas as pd 
import numpy as np 
import time 

# importing spacy and its libraries 
import spacy 
from spacy import displacy
from collections import Counter
#md = spacy.load(en_core_web_md)
#import en_core_web_md

import json 
import itertools
pd.set_option('display.max_colwidth', None)
import pprint 
import requests

# sentiment analysis library
import textblob 
from textblob import TextBlob

# plotting graphs library
import matplotlib.pyplot as plt

import nltk 
import nltk.corpus
from nltk import sent_tokenize, word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta

import finnhub
from datetime import datetime
import datetime as dt
from datetime import timedelta
import dateutil.relativedelta
import streamlit as st 

 try:
      nlp = spacy.load("en_core_web_md")
  except: # If not present, we download
      spacy.cli.download("en_core_web_md")
      nlp = spacy.load("en_core_web_md")

# defining current time elements
nlp = en_core_web_md.load()
q = 'TSLA'
from_time = '2021-08-01' 
to_time = '2022-07-20'
current_month = datetime.now().month
current_year = datetime.now().year
current_day = datetime.now().day
current_date = str(current_year)+'-'+str(current_month)+'-'+str(current_day)
#current_date = pd.to_datetime(current_date)
print(current_date)
current_date = str(current_date)

# defining the functions for finnhub
api_key = 'cbcgogiad3ib4g5ulrb0'
sandbox_key = 'sandbox_cbcgogiad3ib4g5ulrbg'
finnhub_client = finnhub.Client(api_key=api_key)

# making a list of the last 15 days 
print
response =  finnhub_client.company_news('TSLA',_from='2022-10-08', to='2022-11-08')
response_str = ' '.join(map(str, response))

# making a list of lists 
title_list =[]
date_list = []
desc_list = []
sent_list = []
date_real_list = []
sent_1_list = []

for i in response:
  title = list(i.values())[2]
  timestamp = list(i.values())[1]
  summ = list(i.values())[7]
  sent = TextBlob(title).sentiment.polarity
  sent_1 = TextBlob(summ).sentiment.polarity
  title_list.append(title)
  date_list.append(timestamp)
  desc_list.append(summ)
  sent_list.append(sent)
  sent_1_list.append(sent_1)

for j in date_list:
  dty_obj=dt.datetime.fromtimestamp(j).strftime('%d-%m-%y')
  date_real_list.append(dty_obj)


df_y = pd.DataFrame()
df_y['Title'] = title_list
df_y['Summary'] = desc_list
df_y['Sentiment'] = sent_list
df_y['date'] = date_list
df_y['Sentiment_summ'] = sent_1_list

# converting the columns to datetime 
df_y['date'] = pd.to_datetime(df_y['date'],unit = 's').dt.date

# we need to reorder the date structure 

title_date_sent = df_y.groupby('date')['Sentiment_summ'].mean()
title_date_sent = pd.DataFrame(title_date_sent)
print(title_date_sent)

# finding the delta performing summary and title


# for spacy will only be run on the last month of the final requirem
# extraction of spacy library information from the df
def spacy(news_str):
  #remove punctuations from the string
  punctuations = '''!()-[]\{};:'"/,<>./?@#$%^&*_~]1234567890''' #list of all the punctuations we remove from the list
  news_str_mt = ""
  for char in news_str:
      if char not in punctuations:
          news_str_mt = news_str_mt + char
  #creating the string into a list
  news_list_space= news_str_mt.split(" ")
  news_list_punc= []
  for i in news_list_space:
    if i is not '':
      news_list_punc.append(i)
  #removing the stopwords from the list
  stop_str= "rt RT shall \n a about above across after afterwards again against all almost alone along already also although always am among amongst amoungst amount an and another any anyhow anyone anything anyway anywhere are around as at back be became because become becomes becoming been before beforehand behind being below beside besides between beyond bill both bottom but by call can cannot cant co computer con could couldnt cry de describe detail do done down due during each eg eight either eleven else elsewhere empty enough etc even ever every everyone everything everywhere except few fifteen fify fill find fire first five for former formerly forty found four from front full further get give go had has hasnt have he hence her here hereafter hereby herein hereupon hers herse him himse his how however hundred i ie if in inc indeed interest into is it its itse keep last latter latterly least less ltd made many may me meanwhile might mill mine more moreover most mostly move much must my myse name namely neither never nevertheless next nine no nobody none noone nor not nothing now nowhere of off often on once one only onto or other others otherwise our ours ourselves out over own part per perhaps please put rather re same see seem seemed seeming seems serious several she should show side since sincere six sixty so some somehow someone something sometime sometimes somewhere still such system take ten than that the their them themselves then thence there thereafter thereby therefore therein thereupon these they thick thin third this those though three through throughout thru thus to together too top toward towards twelve twenty two un under until up upon us very via was we well were what whatever when whence whenever where whereafter whereas whereby wherein whereupon wherever whether which while whither who whoever whole whom whose why will with within without would yet you your yours yourself yourselves"
  stop_list= stop_str.split(" ")
  news_list_stop=[]
  #removing the stopwords from the sentences
  for j in news_list_punc:
    if j not in stop_list:
      news_list_stop.append(j)
  #removing the stopwords from the sentences
  news_stop_str = " "
  for char in news_str_mt:
    if char not in stop_str:
      news_stop_str = news_stop_str + char
  #stemming the words
  s_stemmer = SnowballStemmer(language='english') #setting the language
  news_stem=[]
  for word in news_list_stop:
      news_stem.append(s_stemmer.stem(word))

  news_list_count= Counter(news_stem)

  #converting the dictionary into a list 
  keys= news_list_count.keys()
  values= news_list_count.values()

  #converting the list into a df 
  tweets_df= pd.DataFrame({'count':values,'keywords': keys})

  #we can order the pandas df in descending order
  tweets_df = tweets_df.sort_values(by=['count','keywords'], ascending = False)
  print(tweets_df.head(10))

  #Making the spacy library work
  doc = nlp(news_str)
  print(len(doc))

  label = [(X.text, X.label_) for X in doc.ents]

  df_1 = pd.DataFrame(label, columns = ['word','entity'])

  # getting Country values in spacy
  df_2 = df_1.where(df_1['entity'] == 'NORP')
  df_2 = df_2['word'].value_counts().nlargest(10)
  print(df_2)
  
  # the people mentioned in the news
  df_3 = df_1.where(df_1['entity']== 'PERSON')
  df_3 = df_3['word'].value_counts().nlargest(10)
  print('the people/products mentioned have been')
  print(df_3)

  # the organisations mentioned in the news
  df_4 = df_1.where(df_1['entity']=='ORG')
  df_4 = df_4['word'].value_counts().nlargest(10)
  print("The Organisations mentioned have been ")
  print(df_4)

  df_5 = df_1.where(df_1['entity']== 'EVENT')
  df_5 = df_5['word'].value_counts().nlargest(10)
  print("The Events mentioned were")
  print(df_5)


# converting the summary into a string 
news_list = df_y['Summary'].to_list()
news_list
news_str = ' '.join(map(str, news_list))
news_str

spacy(news_str)

st.write(f'The current date is {current_date}')
st.table(title_date_sent)
st.write(news_str)
