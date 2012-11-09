import pymongo as mongo
from classifier import *
from process import categorize

conn = mongo.Connection()
db = conn.CompProb
tweets = db.tweets
trainer = db.trainer
words = db.words
priors = count_sentiment(trainer)

#SELF_DESTRUCT(tweets, trainer, words)
cursor = tweets.find()



i = 0
# # while i < 4:
for tweet in cursor:
	i += 1
	cat = categorize(tweet['text'].lower())
	tweet['category'] = cat
# 	tweet['max_sentiment'] = determine_sentiment(tweet['sentiment_stats'])
	tweets.save(tweet)
	if i % 1000 == 0:
		print i
# tweet = tweets.find_one()
# print tweet['text']
# text = split_tweet(tweet['text'])
# print text
# result = classify(text, priors, words)
# print result
# sentiment = determine_sentiment(result)
# print sentiment
# #i += 1



