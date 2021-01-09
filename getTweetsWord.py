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


'''
Date_until should be in format YYYY-MM-D
'''
def getTweetsSnscrape(Date_until_Year, Date_until_month, Date_until_day, nbrDays):

	tweets_list1 = []


	# Using TwitterSearchScraper to scrape data and append tweets to list
	# stri = 'bitcoin since:'+ '2020-01-01' +' until:' + '2020-12-31'
	dayDelta = datetime.timedelta(days=-1)
	date2 = datetime.date(Date_until_Year,Date_until_month,Date_until_day)
	date1 = date2 + dayDelta

	n=0
	while( n <= nbrDays ):
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

if __name__ == "__main__":
	
	getTweetsSnscrape(2021,1,1,365)