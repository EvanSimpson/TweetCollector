'''
This file includes code to:
Analyze the text content of a tweet object to build a training set using frequency analysis.
Naive Bayes classifier used for sentiment analysis.
'''

import pymongo as mongo
import geo
import simplejson as json
import time






keep = ['no', 'ok', 'up']
exclude = set(["2012 election","presidential election","presidential debate","US president","obama administration","president of the united states","republican","ron paul","mitt romney","mitt","romney","democrat","democrats","democratic","barack obama","obama", "barack",
"about","after","all","also","and","another","any","are","because","been","before","being","between","both","came","come","could","each","for","from","get","got","has","had","have","her","here","him","himself","his","how","into","like","make","many","might","more","most","much","must","now","only","other","our","out","over","said","same","see","should","since","some","still","such","take","than","that","the","their","them","then","there","these","they","this","those","through","too","under","very","was","way","well","were","what","where","which","while","who","with","would","you","your"])
categories = { "Democratic Party": ["democrat","democrats","democratic", "barack obama", "darcy richardson", "randall terry"], "Republican Party":["republican", "michele bachman", "herman cain", "newt gingrich", "jon huntsman", "gary johnson", "ron paul", "rick perry", "mitt romney", "rick santorum"], "Barack Obama":["barack obama", "obama"], "Darcy Richardson": ["darcy richardson"], "Randall Terry": ["randall terry"], "Michele Bachmann": ["michele bachmann"], "Herman Cain": ["herman cain"], "Newt Gingrich": ["newt gingrich"], "Jon Huntsman": ["jon hunstman"], "Gary Johnson": ["Gary Johnson"], "Ron Paul": ["ron paul"], "Rick Perry": ["rick perry"], "Mitt Romney": ["mitt romney", "romney"], "Rick Santorum": ["rick santorum"] }


######## REMOVE @'s and HASHTAGS #



	
def split_tweets(tagged_tweet):
	'''
		Split tweets into individual words and remove any noise words.
	'''
	words_filtered = set([e.lower() for e in tagged_tweet.split() if len(e) >= 3 or e in keep])
	temp = list(words_filtered)
	for word in exclude:
		if word in words_filtered:
			temp.remove(word)
	words_filtered = set(temp)
	for word in words_filtered:
		if '@' in word or '#' in word:
			temp.remove(word)
	filtered_tweet = temp
	return filtered_tweet



def update_word(word, sentiment, collection):
	dbword = word_collection.find_one({'word': word})
	if dbword:
		if sentiment == 'positive':
			dbword['positive'] += 1
		elif sentiment == 'negative':
			dbword['negative'] += 1
		else:
			dbword['neutral']  += 1
		dbword['count'] += 1
		word_collection.save(dbword)
	else:
		new_word = {'word': word, 'count': 1}
		if sentiment == 'positive':
			new_word['positive'] = 1
			new_word['negative'] = 0
			new_word['neutral'] = 0
		elif sentiment == 'negative':
			new_word['negative'] = 1
			new_word['positive'] = 0
			new_word['neutral'] = 0
		else:
			new_word['positive'] = 0
			new_word['negative'] = 0
			new_word['neutral'] = 1
		word_collection.insert(new_word)






def tag_words(tweet_words, sentiment, collection):
	for word in tweet_words:
		update_word(word, sentiment, collection)


def build_training_set(collection1, collection2):
	li = 0
	cursor = collection1.find()
	for tweet in cursor:
		li += 1
		print li
		text = tweet['text']
		sentiment = tweet['sentiment']
		filtered_tweet = split_tweets(text)
		tag_words(filtered_tweet, sentiment, collection2)



			



if __name__ == '__main__':
	connection = mongo.Connection()
	db = connection.CompProb
	tweets_collection = db.tweets
	trainer_collection = db.trainer
	#tweets_collection.find_one({'geo': {'$ne' : None}})
	word_collection = db.words
	trainer_collection.create_index([("word", mongo.DESCENDING)])
	#build_training_set(trainer_collection, word_collection)




