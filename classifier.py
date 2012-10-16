#Naive Bayes classifier used for sentiment analysis.

import pymongo as mongo
import geo
import simplejson as json
import time






keep = ['not', 'yes', 'no', 'bad', 'ok', 'why', 'how', 'can']
exclude = ["this", "that", "2012 election","presidential election","presidential debate","US president","obama administration","president of the united states","republican","ron paul","mitt romney","mitt","romney","democrat","democrats","democratic","barack obama","obama", "barack"]
categories = { "Democratic Party": ["democrat","democrats","democratic", "barack obama", "darcy richardson", "randall terry"], "Republican Party":["republican", "michele bachman", "herman cain", "newt gingrich", "jon huntsman", "gary johnson", "ron paul", "rick perry", "mitt romney", "rick santorum"], "Barack Obama":["barack obama", "obama"], "Darcy Richardson": ["darcy richardson"], "Randall Terry": ["randall terry"], "Michele Bachmann": ["michele bachmann"], "Herman Cain": ["herman cain"], "Newt Gingrich": ["newt gingrich"], "Jon Huntsman": ["jon hunstman"], "Gary Johnson": ["Gary Johnson"], "Ron Paul": ["ron paul"], "Rick Perry": ["rick perry"], "Mitt Romney": ["mitt romney", "romney"], "Rick Santorum": ["rick santorum"] }









	
def split_tweets(tagged_tweet):
	filtered_tweet = []

	for words, sentiment in tagged_tweets:
		words_filtered = [e.lower() for e in words.split() if len(e) >= 3 || e in keep]
		for word in exclude:
			if word in words_filtered:
				words_filtered.remove(word)
		filtered_tweet.append((words_filtered, sentiment))
	return filtered_tweet




if __name__ == '__main__':
	connection = mongo.Connection()
	db = connection.CompProb
	tweets_collection = db.tweets
	tweets_collection.find_one({'geo': {'$ne' : None}})



