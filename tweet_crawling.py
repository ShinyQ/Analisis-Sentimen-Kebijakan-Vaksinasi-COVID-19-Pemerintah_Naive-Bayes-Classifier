from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import pandas as pd
import csv
import os
import time
from configparser import ConfigParser

config = ConfigParser()
config.read('tweet_key.ini')

access_token = config.get('key', 'access_token')
access_token_secret = config.get('key', 'access_token_secret')
consumer_key = config.get('key', 'consumer_key')
consumer_secret = config.get('key', 'consumer_secret')

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def scraptweets(search_words, date_since, date_until, numTweets):

    db_tweets = pd.DataFrame(columns=[
                                      'username', 'acctdesc', 'location', 'following',
                                      'totaltweets', 'usercreatedts', 'tweetcreatedts',
                                      'retweetcount', 'text', 'hashtags', 'followers',
                                     ])
    program_start = time.time()

    tweets = tweepy.Cursor(
                    api.search, q=search_words, lang="id", 
                    since=date_since,  tweet_mode='extended').items(numTweets)

    tweet_list = [tweet for tweet in tweets]

    for tweet in tweet_list:
        username = tweet.user.screen_name
        acctdesc = tweet.user.description
        location = tweet.user.location
        following = tweet.user.friends_count
        followers = tweet.user.followers_count
        totaltweets = tweet.user.statuses_count
        usercreatedts = tweet.user.created_at
        tweetcreatedts = tweet.created_at
        retweetcount = tweet.retweet_count
        hashtags = tweet.entities['hashtags']

        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:
            text = tweet.full_text

        ith_tweet = [
                        username, acctdesc, location, following, followers, totaltweets,
                        usercreatedts, tweetcreatedts, retweetcount, text, hashtags
                    ]

        db_tweets.loc[len(db_tweets)] = ith_tweet

        filename = 'covid_vaccine_tweets.csv'
        db_tweets.to_csv(filename, index=False)

    program_end = time.time()
    print('Scraping has completed!')
    print('Total time taken to scrap is {} minutes.'.format(round(program_end - program_start)/60, 2))


search_words = "#vaksin OR #vaksincovid19 OR #vaksincovid OR #VaksinUntukKita OR #vaksingratis"
date_since = "2020-12-01"
date_until = "2020-12-02"
numTweets = 1000

scraptweets(search_words, date_since, date_until, numTweets)
