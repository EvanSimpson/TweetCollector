'''
	Distributions
	Plotting
'''

import pymongo as mongo
import random


def make_cdf(sample_set, target_value):
	'''
		Get the cumulative probability for values in the set being below the given value.
	'''
	count = 0.0
	for value in sample_set:
		if value <= target_value:
			count += 1.0
	return count/len(sample_set)


def run_cdf(whole_set):
	sample_set = random.sample(whole_set, 100000)
	buckets = range(0, max(sample_set), 30)
	results = []
	for i in buckets:
		results.append(make_cdf(sample_set, i))
	return (results, buckets)


def cdf_crazy(whole_set):
	cdfs = []
	for i in range(1000):
		cdfs.append(run_cdf(whole_set))
	return cdfs


if __name__ == "__main__":
	conn = mongo.Connection()
	db = conn.CompProb
	tweets = db.tweets
	rats = tweets.find({'max_sentiment': 'pos', 'category': 'Mitt Romney'})
	# cdf = {}
	# for tweet in rats:
	# 	if tweet['following'] > 0:
	# 		ratio = float(tweet['followers'])/tweet['following']
	# 	else:
	# 		ratio = 0
	# 	if ratio > 10:
	# 		cdf['veryHigh'] = cdf.get('veryHigh', 0) + 1
	# 	elif ratio > 1:
	# 		cdf['high'] = cdf.get('high', 0) + 1
	# 	elif ratio > .5:
	# 		cdf['mid'] = cdf.get('mid', 0) + 1
	# 	elif ratio > .25:
	# 		cdf['low'] = cdf.get('low', 0) + 1
	# 	else:
	# 		cdf['veryLow'] = cdf.get('veryLow', 0) + 1
	# print cdf
	followers = []
	for tweet in rats:
		followers.append(tweet['followers'])
	x = run_cdf(followers)
	print x