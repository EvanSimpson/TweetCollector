'''
This file includes code to:
Analyze the text content of a tweet object to build a training set using frequency analysis.
Naive Bayes classifier used for sentiment analysis.
'''

import pymongo as mongo
import geo
import simplejson as json
import time

connection = mongo.Connection()
db = connection.CompProb
word_collection = db.words


keep = ['no', 'ok', 'up']
exclude = set(["2012 election","presidential election","presidential debate","US president","obama administration","president of the united states","republican","ron paul","mitt romney","mitt","romney","democrat","democrats","democratic","barack obama","obama", "barack",
"about","after","all","also","and","another","any","are","because","been","before","being","between","both","came","come","could","each","for","from","get","got","has","had","have","her","here","him","himself","his","how","into","like","make","many","might","more","most","much","must","now","only","other","our","out","over","said","same","see","should","since","some","still","such","take","than","that","the","their","them","then","there","these","they","this","those","through","too","under","very","was","way","well","were","what","where","which","while","who","with","would","you","your"])
categories = { "Democratic Party": ["democrat","democrats","democratic", "barack obama", "darcy richardson", "randall terry"], "Republican Party":["republican", "michele bachman", "herman cain", "newt gingrich", "jon huntsman", "gary johnson", "ron paul", "rick perry", "mitt romney", "rick santorum"], "Barack Obama":["barack obama", "obama"], "Darcy Richardson": ["darcy richardson"], "Randall Terry": ["randall terry"], "Michele Bachmann": ["michele bachmann"], "Herman Cain": ["herman cain"], "Newt Gingrich": ["newt gingrich"], "Jon Huntsman": ["jon hunstman"], "Gary Johnson": ["Gary Johnson"], "Ron Paul": ["ron paul"], "Rick Perry": ["rick perry"], "Mitt Romney": ["mitt romney", "romney"], "Rick Santorum": ["rick santorum"] }


######## REMOVE @'s and HASHTAGS #



	
def split_tweet(tweet):
	'''
		Split tweets into individual words and remove any noise words.
	'''
	words_filtered = set([e.lower().strip('\'\".:;?!,*~()[]{}\\/') for e in tweet.split() if len(e) >= 3 or e in keep])
	temp = list(words_filtered)
	for word in exclude:
		if word in words_filtered:
			temp.remove(word)
	words_filtered = set(temp)
	for word in words_filtered:
		if '@' in word or '#' in word or 'http' in word:
			temp.remove(word)
	filtered_tweet = temp
	return filtered_tweet



def update_word(word, sentiment):
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



def count_sentiment(collection):
	cursor = collection.find()
	sentDict = {'positive': 0, 'negative' : 0,'neutral' : 0}
	for tweet in cursor:
		sentiment = tweet['sentiment']
		if sentiment == 'positive':
			sentDict['positive'] += 1
		elif sentiment == 'negative':
			sentDict['negative'] += 1
		else:
			sentDict['neutral']  += 1
	return sentDict



def normalize_dict(dic):
	'''
		Returns a new dictionary with normalized values.
	'''
	total = float(sum(dic.values()))
	if total == 0:
		total = 1
	new_dic = {}
	for key in dic:
		new_dic[key] = dic[key] / total
	new_dic['total'] = total
	return new_dic


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
		filtered_tweet = split_tweet(text)
		tag_words(filtered_tweet, sentiment, collection2)

def build_test_set(collection):
	cursor = collection.find()
	for tweet in cursor:
		tweet['tweet_words'] = split_tweet(tweet['text'])
		collection.save(tweet)

def determine_sentiment(sent_dict):
	'''
		Use this function to return the sentiment value with the highest probability.
	'''
	if 'total' in sent_dict:
		sent_dict.pop('total')
	v=list(sent_dict.values())
	k=list(sent_dict.keys())
	return k[v.index(max(v))]


def sum_dictionaries(prob_dict):
	'''
		Adds up all of the positive, negative, and neutral probabilities in a dictionary of dictionaries.
		Returns the normalized sums.
	'''
	pos = 0
	neg = 0
	neu = 0
	for word in prob_dict:
		#print word
		pos += prob_dict[word]['pos']
		neg += prob_dict[word]['neg']
		neu += prob_dict[word]['neu']
	return normalize_dict({'pos':pos, 'neg':neg,'neu':neu})


def bayesify_word(word, prior, collection):
	'''
		Uses bayes rule to find the probability of a given word being positive, negative, or neutral.
		Returns a normalized dictionary of these probabilities.
	'''
	dbword = collection.find_one({'word': word})
	if dbword:
		word_probs = {}
		word_probs['pos'] = (dbword['positive'] / float(dbword['count'])) * (dbword['positive'] / float(prior['positive']))
		word_probs['neg'] = (dbword['negative'] / float(dbword['count'])) * (dbword['negative'] / float(prior['negative']))
		word_probs['neu'] = (dbword['neutral']  / float(dbword['count'])) * (dbword['neutral']  / float(prior['neutral']) )
		return normalize_dict(word_probs)
	else:
		return False


def classify(tweet, priors, collection):
	'''
		Finds the probability of a tweet being positive, negative, or neutral.
		Return a normalized dictionary of probabilities.
	'''
	words_sentiment = {}
	unclassified_words = []
	max_sentiment = False
	for word in tweet:
		sentiment = bayesify_word(word, priors, collection)
		if sentiment:
			words_sentiment[word] = sentiment
			#print "Sentiment of " + word+ ": " + str(sentiment)
		else:
			unclassified_words.append(word)
	if words_sentiment != {}:
		return (sum_dictionaries(words_sentiment), unclassified_words)
	else:
		return False


def SELF_DESTRUCT(tweets_collection, trainer_collection, word_collection):
	'''
		This function will process all 1,059,748 stored in the database.
		Run at your own risk. Good luck. We're all counting on you.
	'''
	priors = count_sentiment(trainer_collection)
	cursor = tweets_collection.find()
	count = 0
	for tweet in cursor:
		count += 1
		text = split_tweet(tweet['text'])
		result = classify(text, priors, word_collection)
		if result:
			max_sentiment = determine_sentiment(result[0])
			if result[1] != []:
				for word in result[1]:
					update_word(word, max_sentiment)
			tweet['sentiment_stats'] = result[0]
			tweet['max_sentiment'] = max_sentiment
		tweets_collection.save(tweet)
		if count % 1000 == 0:
			print count




if __name__ == '__main__':
	connection = mongo.Connection()
	db = connection.CompProb
	tweets_collection = db.tweets
	trainer_collection = db.trainer
	#tweets_collection.find_one({'geo': {'$ne' : None}})
	word_collection = db.words
	word_collection.create_index([("word", mongo.DESCENDING)])
	#build_training_set(trainer_collection, word_collection)
	#priors = count_sentiment(trainer_collection)
	




