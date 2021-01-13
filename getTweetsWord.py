import csv
import datetime
import json
import re
import sys, os 

import pandas as pd
import snscrape.modules.twitter as sntwitter
import tweepy

from preprocessingTweets import format_semantic, format_syntax, remove_noise, process_tweets


'''
Date_until should be in format YYYY-MM-D
'''
def getTweetsSnscrape(Date_until_Year, Date_until_month, Date_until_day, nbrDays, nbrTweetsPerDay, outputFilename, mot):

	tweets_list1 = []


	# Using TwitterSearchScraper to scrape data and append tweets to list
	# stri = 'bitcoin since:'+ '2020-01-01' +' until:' + '2020-12-31'
	dayDelta = datetime.timedelta(days=-1)
	date2 = datetime.date(Date_until_Year,Date_until_month,Date_until_day)
	date1 = date2 + dayDelta

	n=1
	while( n <= nbrDays ):
		for i,tweet in enumerate(sntwitter.TwitterSearchScraper(mot +' since:'+ str(date1) +' until:' + str(date2)).get_items()):
			if i>nbrTweetsPerDay:														
				break
			tmp = ""
			tmp=tweet.content
			tmp = remove_noise(tmp)
			# tmp = process_tweets(tmp)
			# tmp = format_syntax(tweet.content)
			tweets_list1.append([tweet.date, tmp])

		date1 = date1 + dayDelta
		date2 = date2 + dayDelta
		n+=1
		os.system('clear')

		print(str(n) + " / " + str(nbrDays) )

	# Creating a dataframe from the tweets list above 
	tweets_df1 = pd.DataFrame(tweets_list1, columns=['created_at', 'Text'])

	tweets_df1.to_csv(outputFilename, index=False)


# https://medium.com/better-programming/how-to-scrape-tweets-with-snscrape-90124ed006af

if __name__ == "__main__":
	
	getTweetsSnscrape(2021,1,13,90,300,"./tweets4/newTweets.csv", "#bitcoin")