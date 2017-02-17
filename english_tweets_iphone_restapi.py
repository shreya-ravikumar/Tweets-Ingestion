import sys
import jsonpickle
import os
import tweepy
#use use token and access keys										
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

auth = tweepy.AppAuthHandler(consumer_key,consumer_secret)
 
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
 
if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)
searchQuery = 'apple iphone7 OR #iphone7 OR iphone7Plus OR #iOS10 OR #AppleEvent -filter:retweets' # this is what we're searching for
maxTweets = 100000000 # to search through a large number of tweets 
tweetsPerQry = 100  # this is the max the rest API permits
fName = 'english_iphone_tweets_14-17th.txt' #saves the tweets extracted into file  

sinceId = None

max_id = -1L   #max ID assignmed to a large number

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        if (max_id <= 0):
                if (not sinceId):         #checking tweet_id so that you don't get repeated tweets, tweet_id is a unique for every tweet
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, since='2016-09-14', until='2016-09-17', lang='en')  #you can extra attributes for getting very specific kind of tweets
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, since='2016-09-14', until='2016-09-17',lang='en', since_id=sinceId)   #can extract data upto 7-9days
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,since='2016-09-14', until='2016-09-17', lang='en', max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, since='2016-09-14', until='2016-09-17',lang='en', max_id=str(max_id - 1), since_id=sinceId)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
				f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n') #using pickle object to save python object into character stream so as to save it in a proper format in a file on disk 
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        
print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))   #gives the number of tweets downloaded when the program is executed 
