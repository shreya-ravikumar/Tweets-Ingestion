import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#user credentials 
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

#basic listener
class StdOutListener(StreamListener):

    def on_data(self, data):
        if 'retweeted_status' not in data and "RT @" not in data:  #removes retweets
		file=open("uselections_tweets_enkotres.txt","a")
		file.write(data)
		file.write("\n")
		file.close()
		print data
        	return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #handles authetification and the connection to stream api
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    stream.filter(track=['#USElections2016','USElections','Hillary Clinton','Donald Trump'],languages=['en','es','tr','ko'])   #language filter and track 
