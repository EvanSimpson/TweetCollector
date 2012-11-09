'''
	Hypothesis testing
	Difference-in-means
	Chi-Square testing
'''

import pymongo as mongo
import random



def diff_means():








if __name__ == "__main__":
	#do stuff
	conn = mongo.Connection()
	db = conn.CompProb
	tweets = db.tweets

	list_of_ids=[]
	number = 50000
	cursor = tweets.find()
	for item in cursor:
		list_of_ids.append(item['_id'])
	sample = random.sample(list_of_ids, number)