import pymongo as mongo
import simplejson as json


def categorize(text):
	'''
		Takes tweet text as argument, checks for keywords to categorize tweet.
		Returns list of categories found in tweet.
	'''
	tweet_cat = []
	categories = { "Democratic Party": ["democrat","democrats","democratic", "barack obama", "darcy richardson", "randall terry"], "Republican Party":["republican", "michele bachman", "herman cain", "newt gingrich", "jon huntsman", "gary johnson", "ron paul", "rick perry", "mitt romney", "rick santorum"], "Barack Obama":["barack obama", "obama"], "Darcy Richardson": ["darcy richardson"], "Randall Terry": ["randall terry"], "Michele Bachmann": ["michele bachmann"], "Herman Cain": ["herman cain"], "Newt Gingrich": ["newt gingrich"], "Jon Huntsman": ["jon hunstman"], "Gary Johnson": ["Gary Johnson"], "Ron Paul": ["ron paul"], "Rick Perry": ["rick perry"], "Mitt Romney": ["mitt romney", "romney"], "Rick Santorum": ["rick santorum"] }
	for category, terms in categories.items():
		for term in terms:
			if term in text:
				if category not in tweet_cat:
					tweet_cat.append(category)
	return tweet_cat



def buildTweet(jsdata):
	'''
		Converts json tweet data into a python dictionary.
		Returns a dictionary.
	'''
	category = categorize(jsdata["text"])
	tweetd = {
		"iso_language_code" : jsdata["iso_language_code"],
		"to_user_name" : jsdata["to_user_name"],
		"from_user_id_str" : jsdata["from_user_id_str"],
		"text" : jsdata["text"],
		"created_at" : jsdata["created_at"],
		"profile_image_url" : jsdata["profile_image_url"],
		"to_user_id_str" : jsdata["to_user_id_str"],
		"to_user" : jsdata["to_user"],
		"source" : jsdata["source"],
		"id_str" : jsdata["id_str"],
		"from_user_name" : jsdata["from_user_name"],
		"from_user" : jsdata["from_user"],
		"tweet_id" : jsdata["id"],
		"from_user_id" : jsdata["from_user_id"],
		"to_user_id" : jsdata["to_user_id"],
		"geo" : jsdata["geo"],
		"profile_image_url_https" : jsdata["profile_image_url_https"],
		"metadata" : jsdata["metadata"],
		"category" : category
		}
	return tweetd



def addTweet(tweetd):
	'''
		Checks that the given tweet dictionary isn't already stored in the database, and then stores it.
		Returns nothing.
	'''
	if tweets_collection.find_one({"tweet_id": tweetd["tweet_id"]}) == None:
		tweets_collection.insert(tweetd)




connection = mongo.Connection()
db = connection.CompProb
tweets_collection = db.tweets
tweets_collection.create_index([("tweet_id", mongo.DESCENDING), ("geo", mongo.DESCENDING), ("from_user_id", mongo.DESCENDING)])
#tweets_collection.insert()
#tweets_collection.find_one({"tweet_id": "1230827349"})
 	



with open('results.json', 'r') as z:
	
	for line in z:
		jstweet = json.loads(line)
		tweetd = buildTweet(jstweet)
		addTweet(tweetd)
		


print "finished"




