# 20230503_Comprehensive Twitter Database Using MySQL and ElasticSearch for Searching Application

- Latest Updated: 20230503
- Readme Edited: 20231209

- Author: Yunhao Li\*, Siheng Huang, Yanhan Chen, Yicong Li

- Description: This project is an group project, which builds a Comprehensive Twitter Database using MySQL and ElasticSearch for Searching Application. The original tweet data was collated and processed, followed by a reconstruction of the retweet data structure. Three relational data stores were established using MySQL to store basic tweet information, user information, and tweet popularity. A non-relational data store was built with ElasticSearch to store the text of all tweets. A cache was set up to store the most popular user data, saving searching time by avoiding the need to pull data from the database repeatedly. A search application was built upon these three components, offering functions such as searching for tweets, users, and the most popular tweets and users.
	- Forked from SIHENG-H/RU_DataBase_Management_694_2023_team15: https://github.com/SIHENG-H/RU_DataBase_Management_694_2023_team15


 - Data Description
	- The utilized dataset is ’corona-out-3’, containing information from 101,894 tweets. This information is stored in a dictionary-like format, which includes data about each tweet such as the posting time, tweet ID, text, source, and user information like user ID, name, location, URL, and creation time. Interactive messages, such as quotes, replies, retweets, and favorites, are also included. A subdictionary records the retweets of each tweet; if a tweet is a retweet, the dictionary value comprises all aforementioned information of the retweeted tweet.
