#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 21:54:43 2024

@author: leahboger
"""
import pandas as pd
from top2vec import Top2Vec
import seaborn as sns
import matplotlib.pyplot as plt

#read in all comments
all_comments_prob = pd.read_csv('/Users/leahboger/Documents/web_scraping/all_comments_prob.csv')


#group probabilities. 3 categories: pro_pc (pc_positive+ console_negative), pro_console (console_positive + pc_negative), neutral (pc_neutral + console_neutral)
#created thresholding so if the max score was nuetral, if the next highest category was less than 0.4 away, it was labeled as next  highest and not neutral
def group_probabilites(row):
    pro_console_score = row['console_positive'] + row['pc_negative'] 
    pro_pc_score = row['pc_positive'] + row['console_negative']
    neutral_score = row['pc_neutral'] + row['console_neutral']
    
    sentiment_dict = {
        'pro_console' : pro_console_score,
        'pro_pc': pro_pc_score,
        'neutral' : neutral_score
        }

    max_sent = max(sentiment_dict, key=sentiment_dict.get)

    # If the max sentiment is neutral, check the differences
    if max_sent == 'neutral':
        difference_pro_pc = abs(neutral_score - pro_pc_score)
        difference_pro_console =  abs(neutral_score - pro_console_score)
        
        # Check if the differences are less than 0.2
        if difference_pro_pc < 0.4 or difference_pro_console < 0.4:
            # Remove 'neutral' from the dictionary and return the next highest sentiment
            sentiment_dict.pop('neutral')
            return max(sentiment_dict, key=sentiment_dict.get)
    
    return max_sent

# apply function
all_comments_prob['comment_type'] = all_comments_prob.apply(group_probabilites, axis=1)

#make text string type
all_comments_prob['text'] = all_comments_prob['text'].astype(str)

# remove rows where 'text' contains one word or less
all_comments_prob = all_comments_prob[all_comments_prob['text'].str.split().str.len() > 1]


#visualize count of comments per comment type
sns.countplot(data=all_comments_prob, x='comment_type')
plt.xlabel('Comment Sentiment')
plt.ylabel('Count')
plt.title('Comment Sentiment by Count')
plt.savefig('/Users/leahboger/Documents/web_scraping/comment_sentiment_by_count.png', dpi=300, bbox_inches='tight')
plt.show()

# expand data based on like count (each like acts as repeat of the comment) -- if negaitve(in case of reddit, counts as if it were 0 likes)
expanded_data = []
for _, row in all_comments_prob.iterrows():
    count = max(row['like_count'], 1)  # Count as 1 if like_count is 0
    expanded_data.extend([row] * count)  # Repeat the row 'count' times

expanded_df = pd.DataFrame(expanded_data)

# plotting the data
sns.countplot(data=expanded_df, x='comment_type')
plt.xlabel('Comment Sentiment')
plt.ylabel('Count')
plt.title('Comment Sentiment by Count')
plt.savefig('/Users/leahboger/Documents/web_scraping/expanded_comment_sentiment_by_count.png', dpi=300, bbox_inches='tight')
plt.show()


# side by side box plot of averge comment length

all_comments_prob['word_count'] = all_comments_prob['text'].apply(lambda x: len(x.split()))

box_data = [all_comments_prob[all_comments_prob['comment_type'] == t]['word_count'] for t in all_comments_prob['comment_type'].unique()]

# Plot side-by-side box plots of word count
plt.figure(figsize=(8, 6))
plt.boxplot(box_data, labels=all_comments_prob['comment_type'].unique(), patch_artist=True)
plt.title('Box Plot of Word Count by Type')
plt.xlabel('Type')
plt.ylabel('Word Count')
plt.savefig('/Users/leahboger/Documents/web_scraping/word_count_by_type.png', dpi=300, bbox_inches='tight')
plt.show()

#plot isde by side hist of like count
boxplot_data = [all_comments_prob[all_comments_prob['comment_type'] == t]['like_count'] for t in all_comments_prob['comment_type'].unique()]

# Step 2: Plot the box plot
plt.figure(figsize=(8, 6))
plt.boxplot(boxplot_data, labels=all_comments_prob['comment_type'].unique(), patch_artist=True)
plt.title('Box Plot of Like Count by Comment Type')
plt.xlabel('Comment Type')
plt.ylabel('Like Count')
plt.savefig('/Users/leahboger/Documents/web_scraping/like_count_by_type.png', dpi=300, bbox_inches='tight')

plt.show()

#remove comments with word count > 400 unless like count is greater than 25
filtered_comments = all_comments_prob[~((all_comments_prob['word_count'] > 400) & (all_comments_prob['like_count'] <= 15))]



#side by side box plots of word count
filt_box_data = [filtered_comments[filtered_comments['comment_type'] == t]['word_count'] for t in all_comments_prob['comment_type'].unique()]

plt.figure(figsize=(8, 6))
plt.boxplot(filt_box_data, labels=all_comments_prob['comment_type'].unique(), patch_artist=True)
plt.title('Box Plot of Average Word Count by Type')
plt.xlabel('Type')
plt.ylabel('Word Count')
plt.savefig('/Users/leahboger/Documents/web_scraping/filtered_word_count_by_type.png', dpi=300, bbox_inches='tight')
plt.show()

#expand filtered data
#expanded_filtered = []
#for _, row in filtered_comments.iterrows():
    #count = max(row['like_count'], 1)  # Count as 1 if like_count is 0
    #expanded_filtered.extend([row] * count)  # Repeat the row 'count' times

#expanded_filtered_coms = pd.DataFrame(expanded_filtered)



# pre-process text 

#Drop unnecessary columns
comments_stripped = filtered_comments.drop(columns=['console_negative', 'console_neutral', 'console_positive', 'pc_negative', 'pc_neutral', 'pc_positive', 'word_count'], axis=1)

# lowercase and remove punctuation

import re
# remove punctuation
comments_stripped['text_processed'] = comments_stripped['text'].map(lambda x: re.sub('[,\.!?]', '', x))
# convert the text to lowercase
comments_stripped['text_processed'] = comments_stripped['text_processed'].map(lambda x: x.lower())


# Import the wordcloud library
from wordcloud import WordCloud
#join all comments
long_string = ','.join(list(comments_stripped['text_processed'].values))
# Create a WordCloud object
wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue')
# Generate a word cloud
wordcloud.generate(long_string)

wordcloud.to_file('/Users/leahboger/Documents/web_scraping/cloud_pre_processing.png') 
# Visualize the word cloud
wordcloud.to_image()


# Define the words to remove
words_to_remove = r'(?i)\b(pc|console|gaming|play|consoles|game|player|games|gamer)\b'
# Remove the specified words from the 'text_processed' column
comments_stripped['text_processed'] = comments_stripped['text_processed'].str.strip().replace(words_to_remove, '', regex=True)



### tockenize, remove stopwords
import gensim
from gensim.utils import simple_preprocess
import nltk
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) 
             if word not in stop_words] for doc in texts]
data = comments_stripped.text_processed.values.tolist()
data_words = list(sent_to_words(data))
# remove stop words
data_words = remove_stopwords(data_words)


#create dictionary
import gensim.corpora as corpora
# Create Dictionary
id2word = corpora.Dictionary(data_words)
# Create Corpus
texts = data_words
# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]



#print top 50 words
word_freq = {}
for doc in corpus:
    for word_id, count in doc:
        word = id2word[word_id]  # Get the word from the dictionary
        word_freq[word] = word_freq.get(word, 0) + count

# Sort the words by frequency (descending order)
sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)


# Display the top 50 words (or fewer if the corpus is small)
top_50_words = sorted_word_freq[:50]


# Print the top 50 most frequent words
for word, freq in top_50_words:
    print(f"{word}: {freq}")


# add words to exclude as stopwords and split into three corpus: pro_pc, pro_console, neutral


pro_console_coms = comments_stripped[comments_stripped['comment_type'] == 'pro_console']
pro_pc_coms = comments_stripped[comments_stripped['comment_type'] == 'pro_pc']
neutral_coms = comments_stripped[comments_stripped['comment_type'] == 'neutral']

stop_words = stopwords.words('english')
stop_words.extend(['like', 'get', 'better', 'players', 'even', 'one', 'want','much', 'people', 'use', 'playing', 'also', 'still', 'would', 'good', 'really', 'need', 'way', 'think', 'go',' every', 'lot', 'always', 'great', 'make', 'thing', 'best', 'never', 'got', 'well', 'back', 'going', 'gamers', 'controller', 'controllers', 'console', 'fconsole', 'ass', 'op', 'getting', 'since', 'dont', 'rather', 'either', 'instead', 'making', 'said', 'anymore', 'come', 'comes'])
#remove sentiment words

from nltk.corpus import opinion_lexicon


positive_words = set(opinion_lexicon.positive())
negative_words = set(opinion_lexicon.negative())

# Combine positive and negative words into the stop words list
stop_words.extend(positive_words)
stop_words.extend(negative_words)

def sent_to_words(sentences):
    for sentence in sentences:
        # deacc=True removes punctuations
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) 
             if word not in stop_words] for doc in texts]

## pc corpus

pc_data = pro_pc_coms.text_processed.values.tolist()
pc_data_words = list(sent_to_words(pc_data))
# remove stop words
pc_data_words = remove_stopwords(pc_data_words)

pc_corpus = [' '.join(words) for words in pc_data_words]



## console corpus

console_data = pro_console_coms.text_processed.values.tolist()
console_data_words = list(sent_to_words(console_data))
# remove stop words
console_data_words = remove_stopwords(console_data_words)

console_corpus = [' '.join(words) for words in console_data_words]


## neutral corpus

neutral_data = neutral_coms.text_processed.values.tolist()
neutral_data_words = list(sent_to_words(neutral_data))
# remove stop words
neutral_data_words = remove_stopwords(neutral_data_words)

neutral_corpus = [' '.join(words) for words in neutral_data_words]



## topic model for each corpus

pc_model = Top2Vec(documents=pc_corpus, speed="learn", workers=8)

pc_model.get_num_topics()

pc_model.hierarchical_topic_reduction(num_topics=5)

pc_topic_sizes, pc_topic_nums = pc_model.get_topic_sizes()


pc_topic_words, pc_word_scores, pc_topic_nums = pc_model.get_topics(3)

for idx, pc_topic in enumerate(pc_topic_nums):
    # Get the words for the current topic
    words = pc_topic_words[idx]

    # Join the words into a long string for the word cloud
    long_string = ' '.join(words)

    # Create and generate the word cloud
    wordcloud = WordCloud(background_color="white", max_words=100, contour_width=3, contour_color='steelblue')
    wordcloud.generate(long_string)

    # Save the word cloud with a unique file name
    file_name = f'wordcloud_pctopic_{pc_topic}.png'
    wordcloud.to_file(f'/Users/leahboger/Documents/web_scraping/{file_name}')

    wordcloud.to_image()

    
## topic model for each corpus

con_model = Top2Vec(documents=console_corpus, speed="learn", workers=8)

con_model.get_num_topics()


con_topic_sizes, con_topic_nums = con_model.get_topic_sizes()


con_topic_words, con_word_scores, con_topic_nums = con_model.get_topics()

# Generate word clouds for the topics
for idx, con_topic in enumerate(con_topic_nums):
    if con_topic == 1:
        continue
    # Get the words for the current topic
    words = con_topic_words[idx]

    # Join the words into a long string for the word cloud
    long_string = ' '.join(words)

    # Create and generate the word cloud
    wordcloud = WordCloud(background_color="white", max_words=1000, contour_width=3, contour_color='steelblue')
    wordcloud.generate(long_string)

    # Save the word cloud with a unique file name
    file_name = f'wordcloud_con_topic_{con_topic}.png'
    wordcloud.to_file(f'/Users/leahboger/Documents/web_scraping/{file_name}')

    wordcloud.to_image()



## topic model for each corpus

neutral_model = Top2Vec(documents=neutral_corpus, speed="learn", workers=8)

neutral_model.get_num_topics()
pc_model.hierarchical_topic_reduction(num_topics=5)


neutral_topic_sizes, neutral_topic_nums = neutral_model.get_topic_sizes()


neutral_topic_words, neutral_word_scores, neutral_topic_nums = neutral_model.get_topics(3)

# Generate word clouds for the topics
for idx, neutral_topic in enumerate(neutral_topic_nums):
    if neutral_topic == 0:
        continue
    # Get the words for the current topic
    words = neutral_topic_words[idx]

    # Join the words into a long string for the word cloud
    long_string = ' '.join(words)

    # Create and generate the word cloud
    wordcloud = WordCloud(background_color="white", max_words=1000, contour_width=3, contour_color='steelblue')
    wordcloud.generate(long_string)

    # Save the word cloud with a unique file name
    file_name = f'wordcloud_neutral_topic_{neutral_topic}.png'
    wordcloud.to_file(f'/Users/leahboger/Documents/web_scraping/{file_name}')

    wordcloud.to_image()



