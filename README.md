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
    - 


  
