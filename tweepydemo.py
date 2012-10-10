import tweepy
from textwrap import TextWrapper
import pymongo as mongo
from authvars import AuthVars



auth1 = tweepy.auth.OAuthHandler(AuthVars.c_key, AuthVars.c_secret)
auth1.set_access_token(AuthVars.a_token, AuthVars.a_secret)
api = tweepy.API(auth1)


class StreamListener(tweepy.StreamListener):
    status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')
    connection = mongo.Connection()
    db = connection.CompProb
    tweets_collection = db.tweets
    def on_status(self, status):
        try:
            tweets_collection.insert({'status':status.text})
            print self.status_wrapper.fill(status.text)
            print '\n %s  %s  via %s\n' % (status.author.screen_name, status.created_at, status.source)
        
        except Exception, e:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass


l = StreamListener()
streamer = tweepy.Stream(auth=auth1, listener=l, timeout=3000000000 )
#setTerms = ["2012 election","presidential election","presidential debate","US president","obama administration","president of the united states","republican","ron paul","mitt romney","mitt","romney","democrat","democrats","democratic","barack obama","obama"]
setTerms = ['hello', 'goodbye', 'goodnight', 'good morning']
streamer.filter(None,setTerms)

















