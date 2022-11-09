# importing all the libraries 
import pandas as pd 
import numpy as np 
import time 

# importing spacy and its libraries 
import spacy 
from spacy import displacy
from collections import Counter
import en_core_web_md

import json 
import itertools
pd.set_option('display.max_colwidth', None)
import pprint 
import requests

# sentiment analysis library
import xgboost as xgb
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
import xgboost
from datetime import datetime
import datetime as dt
from datetime import timedelta
import dateutil.relativedelta


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

# spacy analysis of the current month 
df_spacy = df_concat[df_concat['date'].dt.year == current_year]
df_spacy = df_spacy[df_spacy['date'] >= current_date-dateutil.relativedelta.relativedelta(months=1)]
df_spacy

# converting the summary into a string 
news_list = df_spacy['Summary'].to_list()
news_list
news_str = ' '.join(map(str, news_list))
news_str

spacy(news_str)



