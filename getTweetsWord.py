import csv
import datetime
import json
import re
import sys

import pandas as pd
import snscrape.modules.twitter as sntwitter
import tweepy

from getTwitterHandles import getTwitterHandles
from preprocessingTweets import format_semantic, format_syntax, remove_noise

# Creating list to append tweet data to
tweets_list1 = []

# Using TwitterSearchScraper to scrape data and append tweets to list
# stri = 'bitcoin since:'+ '2020-01-01' +' until:' + '2020-12-31'
dayDelta = datetime.timedelta(days=-1)
date1 = datetime.date(2020,12,31)
date2 = datetime.date(2021,1,1)
n=0
while( n <= 365 ):
	for i,tweet in enumerate(sntwitter.TwitterSearchScraper('bitcoin since:'+ str(date1) +' until:' + str(date2)).get_items()):
		if i>100:														
			break
		tmp = ""
		tmp=tweet.content
		tmp = remove_noise(tmp)
		# tmp = format_syntax(tweet.content)
		tweets_list1.append([tweet.date, tmp])

	date1 = date1 + dayDelta
	date2 = date2 + dayDelta
	n+=1
	print(n)

# Creating a dataframe from the tweets list above 
tweets_df1 = pd.DataFrame(tweets_list1, columns=['created_at', 'Text'])

tweets_df1.to_csv('./tweets3/tweets.csv', index=False)


# https://medium.com/better-programming/how-to-scrape-tweets-with-snscrape-90124ed006af

















with open('./twitter_credentials.json') as cred_data:
	info = json.load(cred_data)
	consumer_key = info['CONSUMER_KEY']
	consumer_secret = info['CONSUMER_SECRET']
	access_key = info['ACCESS_KEY']
	access_secret = info['ACCESS_SECRET']

def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	print("Getting tweets from @" + str(screen_name))
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []  
	bitcointweets = []
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	for tweet in new_tweets:
		if(('bitcoin' in tweet.text) | ('btc' in tweet.text)):
			tweet.text = " ".join(remove_noise(tweet.text))

			tweet.text = format_syntax(tweet.text)

			bitcointweets.append(tweet)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print(f"getting tweets before {oldest}")
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		for tweet in new_tweets:
			if(('bitcoin' in tweet.text) | ('btc' in tweet.text)):
				tweet.text = " ".join(remove_noise(tweet.text))

				tweet.text = format_syntax(tweet.text)

				bitcointweets.append(tweet)
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print(f"...{len(alltweets)} tweets downloaded so far")
	
	#transform the tweepy tweets into a 2D array that will populate the csv 
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in bitcointweets]

	#write the csv  
	with open('./tweets2/'+screen_name + '_tweets.csv', 'w', encoding = 'utf8') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)
	
	pass
# if __name__ == "__main__":
# 	handles =  getTwitterHandles()
	
# 	for handle in handles:
# 		try:
# 			get_all_tweets(str(handle))
		  
# 		except:
# 			pass
