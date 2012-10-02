import pymongo as mongo

connection = Connection()

db = connection.CompProb

tweets_collection = db.tweets

#tweets_collection.insert()
#tweets_collection.find_one({"tweet_id": "1230827349"})
#tweets_collection.create_index([("tweets_id", DESCENDING), ("geo", DESCENDING), ("user_id", DESCENDING)])









