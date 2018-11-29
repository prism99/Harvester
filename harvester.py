#!/usr/bin/env python
"""
  Simple script that uses twitter api to download all tweets of a particular twitter
  account with timestamps. Useful for information gathering 
"""

import thread
import csv
import multiprocessing
from time import sleep
import tweepy
from tweepy import *
from tweepy.streaming import *

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
api = tweepy.API(auth)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)


def tgrabber(tUname,auth,api):
    alltweets = []
    new_tweets = api.user_timeline(screen_name = tUname,count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)

		#all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = tUname,count=200,max_id=oldest)

		#save most recent tweets
        alltweets.extend(new_tweets)

		#update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print "...%s tweets downloaded so far" % (len(alltweets))
        #transform the tweepy tweets into a 2D array that will populate the csv
        outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

	#write the csv
    with open('%s_tweets.csv' % tUname, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)
    pass


d = raw_input("Enter Target Username: ")
tgrabber(d,auth,api)
