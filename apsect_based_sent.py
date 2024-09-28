#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 21:24:06 2024

@author: leahboger
"""

#pip install transformers
#pip install sentencepiece
#pip install torch


import torch.nn.functional as F
from transformers import pipeline
import pandas as pd
import torch


#load data

youtube_comments = pd.read_csv('youtube_comments.csv')


#reddit data
cod_comments = pd.read_csv('/Users/leahboger/Documents/web_scraping/cod_comments.csv')
cyber_comments = pd.read_csv('/Users/leahboger/Documents/web_scraping/cyber_comments.csv')
halo_comments = pd.read_csv('/Users/leahboger/Documents/web_scraping/halo_comments.csv')
general_comments = pd.read_csv('/Users/leahboger/Documents/web_scraping/general_comments.csv')

#make reddit comments all one df
reddit_comments = pd.concat([cod_comments, cyber_comments, halo_comments, general_comments], ignore_index=True)

#rename columns
reddit_comments.rename(columns={'score': 'like_count', 'comment_body': 'text'}, inplace=True)



youtube_comments.rename(columns={'video_id': 'post_title'}, inplace=True)


#reorder and grab cols of interest
youtube_comments = youtube_comments[['like_count', 'text', 'post_title']]
reddit_comments = reddit_comments[['like_count', 'text', 'post_title']]

#combine youtube and reddit comments
all_comments = pd.concat([reddit_comments,youtube_comments])

#replace specific types of console with 'console'
all_comments['text'] = all_comments['text'].str.lower().replace('ps5', 'console', regex=True)

all_comments['text'] = all_comments['text'].str.lower().replace('xbox', 'console', regex=True)

all_comments['text'] = all_comments['text'].str.lower().replace('playstation', 'console', regex=True)
all_comments['text'] = all_comments['text'].str.lower().replace('nintendo', 'console', regex=True)

all_comments['text'] = all_comments['text'].str.lower().replace('ps', 'console', regex=True)



# Load Aspect-Based Sentiment Analysis model
from transformers import AutoTokenizer, AutoModelForSequenceClassification
tokenizer = AutoTokenizer.from_pretrained("yangheng/deberta-v3-base-absa-v1.1")
model = AutoModelForSequenceClassification.from_pretrained("yangheng/deberta-v3-base-absa-v1.1")



#create a funciton to assign prob of sentiment w regards to console
def get_probabilities_console(row):
    text = str(row['text']).lower()
    inputs = tokenizer(f"[CLS] {text} [SEP] {'console'} [SEP]", return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    probs = F.softmax(outputs.logits, dim=1).detach().numpy()[0]
    return pd.Series(probs, index=["console_negative", "console_neutral", "console_positive"])

# Apply the function to each row
probabilities_test_con = all_comments.apply(get_probabilities_console, axis=1)

# Combine with the original DataFrame
results_prob_con = pd.concat([all_comments, probabilities_test_con], axis=1)


#create function to assign prob of sentiment w regards to pc
def get_probabilities_pc(row):
    text = str(row['text']).lower()
    inputs = tokenizer(f"[CLS] {text} [SEP] {'pc'} [SEP]", return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    probs = F.softmax(outputs.logits, dim=1).detach().numpy()[0]
    return pd.Series(probs, index=["pc_negative", "pc_neutral", "pc_positive"])

# Apply the function to each row
probabilities_test_pc = all_comments.apply(get_probabilities_pc, axis=1)

# Combine with the original DataFrame
results_prob_pc = pd.concat([results_prob_con, probabilities_test_pc], axis=1)

#rename df
all_comments_prob = results_prob_pc

all_comments_prob.to_csv('/Users/leahboger/Documents/web_scraping/all_comments_prob.csv', index=False)

