import time
import tweepy
from credentials import *

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)

for i in range(12):
	retweets = tweepy.Cursor(api.search, q='Franz Kafka -filter:retweets', lang='en').items(50)
	for tweet in retweets:
		if not tweet.retweeted:
			try:
				api.create_favorite(tweet.id)
				time.sleep(10)
			except:
				pass
	time.sleep(3600)

