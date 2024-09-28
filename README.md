<h1>PC verus Console: webscraping, aspect-based sentiment analysis, and topic modeling</h1>


<h2>Description</h2>
This project aims to explore the common gaming debate between using a PC versus a Console. Using APIs, we scraped comments from popular subreddits and youtube videos on the subject. After cleaning and wrangling the data, we applied a common aspect-based sentiment model (deberta-v3-base-absa) to the comments. We then created a methodolgy to group comments into "pro console," "pro pc," and "neutral" comments. From there we used Top2Vec to model topics within each category. 
<br />

<h2>Language and Packages Used</h2>

  - <b>Python</b> 
    - <b>pandas</b>
    - <b>googleapiclient.discovery</b>
    - <b>transformers</b>
    - <b>torch</b>
    - <b>top2vec</b>
    - <b>seaborn</b>
    - <b>matplotlib</b>
    - <b>re</b>
    - <b>wordcloud</b>
    - <b>gensim</b>
    - <b>nltk</b>


<h2>Project Overview and Highlights:</h2>

1) Scrape comments from youtube and reddit [View the code](web_scraping_scripts/)
  - Youtube videos:
    - [PC vs Console in 2024... time to ditch PC?](https://www.youtube.com/watch?v=GgJj9Mok9dA)
    - [Finally ENDING the PC Gaming vs Console Debate](https://www.youtube.com/watch?v=4BXOa7Eqzxc)
    - [PC Gaming vs Console - What’s ACTUALLY Better? 🤔](https://www.youtube.com/watch?v=Ko8ubyWDy58)
    - [Call of Duty Warzone is not fair ( PC vs Console )](https://www.youtube.com/watch?v=uMBEvgiKqBs)
 
  - Subreddits:
    -  we scraped from 30+ subreddits (general pc vs console debate, game specific: Halo, Call of Duty, Cyberpunk). All URLs are included in the [reddit_scraping.py](web_scraping_scripts/reddit_scraping.py) file.

  -  Click [here](data/) for scraped data in csv format

2) Apply aspect-based sentiment model [DeBERTa v3](https://huggingface.co/yangheng/deberta-v3-base-absa-v1.1) to comments. See code [here](aspect_based_sent.py)
  - We combined and wrangled data. We also found synonyms for "console," such as "ps5," or "playstation" and changed them to be "console"
  - We created 2 functions to implement this model: one where "console" was the aspect, one where "pc" was the aspect
      - example of "console" function:
        ```python
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

3) Group comments into 3 categories using ABSM scores: Pro PC, Pro Console, Neutral
  - We created a function that sums probabilites as follows:
      - Pro PC (positive pc score + negative console score)
      - Pro Console (positive console score + negative pc socre)
      - Neutral (neutral console score + neutral pc score)
  - This function assigns the comment to the max summative score. There is theresholding in place to assign neutral less frequently
  - function:
      ```python
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
        
      # Check if the differences are less than 0.4
      if difference_pro_pc < 0.4 or difference_pro_console < 0.4:
            # Remove 'neutral' from the dictionary and return the next highest sentiment
            sentiment_dict.pop('neutral')
            return max(sentiment_dict, key=sentiment_dict.get)
    
    return max_sent

    # apply function
    all_comments_prob['comment_type'] = all_comments_prob.apply(group_probabilites, axis=1)



  
