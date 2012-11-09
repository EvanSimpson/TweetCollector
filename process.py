'''
This file contains code to process json files containing twitter data and enter it into a database.
'''



import pymongo as mongo
import simplejson as json

count = 0

def categorize(text):
	'''
		Takes tweet text as argument, checks for keywords to categorize tweet.
		Returns list of categories found in tweet.
	'''
	tweet_cat = []
	categories = { "Democratic Party": ["democrat","democrats","democratic", "barack obama", "barack", "obama", "darcy richardson", "randall terry"], "Republican Party":["republican", "michele bachman", "herman cain", "newt gingrich", "jon huntsman", "gary johnson", "ron paul", "rick perry", "mitt romney", "mitt", "romney", "rick santorum"], "Barack Obama":["barack obama", "obama", "barack"], "Mitt Romney": ["mitt romney", "romney"]}
	for category, terms in categories.items():
		for term in terms:
			if term in text:
				if category not in tweet_cat:
					tweet_cat.append(category)
	return tweet_cat



def buildTweet(jsdata):
	'''
		Reduces information from json tweet data dictionary.
		Returns a dictionary.
	'''
	text = jsdata["text"].encode('ascii', 'ignore')
	category = categorize(text)
	user = jsdata["user"]
	tweetd = {
		"text" : text,
		"hashtags" : jsdata["entities"]["hashtags"],
		"created_at" : jsdata["created_at"],
		"source" : jsdata["source"],
		"id_str" : jsdata["id_str"],
		"tweet_id" : jsdata["id"],
		"geo" : jsdata["geo"],
		"category" : category,
		"user" : user["id"],
		"language" : user["lang"],
		"following" : user["friends_count"],
		"followers" : user["followers_count"],
		"verified" : user["verified"],
		"profile_background_color" : user["profile_background_color"],
		"statuses_count" : user["statuses_count"],
		"listed_count" : user["listed_count"]
		}
	try:
		tweetd["retweet_id"] = jsdata["retweeted_status"]["id"]
	except:
		pass
	return tweetd


def buildTweet_fromDataSift(dsdata):
	'''
		Converts json tweet data into a python dictionary.
		Returns a dictionary.
	'''
	jsdata = dsdata["twitter"]
	tweetd = {
		"text" : dsdata["interaction"]["content"].encode('ascii', 'ignore'),
		"id_str" : jsdata["id"],
		"tweet_id" : int(jsdata["id"]),
		"salience" : dsdata["salience"]["content"]["sentiment"],
		"datasift" : 'True'
		}
	if tweetd['salience'] > 0:
		tweetd['sentiment'] = 'positive'
	elif tweetd['salience'] == 0:
		tweetd['sentiment'] = 'neutral'
	else:
		tweetd['sentiment'] = 'negative'
	return tweetd


def addTweet(tweetd, collection):
	'''
		Checks that the given tweet dictionary isn't already stored in the database, and then stores it.
		Returns nothing.
	'''
	if collection.find_one({"tweet_id": tweetd["tweet_id"]}) == None:
		collection.insert(tweetd)


def run_process_training(collection):
	#li = 0
	with open('datasift3.json', 'r') as z:
		
		for line in z:
			#li += 1
			#print li
			jstweet = json.loads(line)
			if "salience" in jstweet.keys():
				try:
					z = jstweet['facebook']
				except:
					tweetd = buildTweet_fromDataSift(jstweet)
					if tweetd:
						addTweet(tweetd, collection)

def run_process(collection):
	with open('results13.json', 'r') as z:
		
		for line in z:
			jstweet = json.loads(line)
			try:
				tweetd = buildTweet(jstweet) 
				try:
					addTweet(tweetd, collection)
				except:
					print "Tweet not added, see what happened."
			except:
				print jstweet
	


if __name__ == '__main__':
	connection = mongo.Connection()
	db = connection.CompProb
	tweets_collection = db.tweets
	tweets_collection.create_index([("tweet_id", mongo.DESCENDING), ("geo", mongo.DESCENDING), ("from_user_id", mongo.DESCENDING)])
	#tweets_collection.insert()
	#tweets_collection.find_one({"tweet_id": "1230827349"})
	trainer_collection = db.trainer
	trainer_collection.create_index([("tweet_id", mongo.DESCENDING)])
	run_process_training(trainer_collection)
	#run_process(tweets_collection)