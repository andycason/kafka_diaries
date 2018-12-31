import tweepy
import nltk
import datetime
import time
from datetime import date
from dateutil import relativedelta
from nltk import word_tokenize, sent_tokenize
from credentials import *

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)

#getting the date in the right format to search kafka.txt

d = date.today()

d_format = d.strftime("%d %B.")

#d_format = "30 December."

if d_format[0] == "0":
	d_format = d_format[1:]
	

#Opening up the kafka.txt file here

k_raw = open('/home/pi/kafka/kafka.txt', 'rU').read().decode('ascii','ignore')

k_sents = sent_tokenize(k_raw)

#find diary entries for today's date
#find first sentence
k_today_loc = k_sents.index(d_format)

print("Found the date in the following location: "+str(k_today_loc))

#find last sentence
next = []

nextmonth = datetime.date.today() + relativedelta.relativedelta(months=1)

for i in k_sents[k_today_loc+1:k_today_loc+100]:
	if d.strftime("%B.") in i:
		next.append(k_sents.index(i))
	if nextmonth.strftime("%B.") in i:
		next.append(k_sents.index(i))

end = next[0]

print("Found the end of the entry in the following location: "+str(end))

#make the tweet

tweet_list = []

for i in k_sents[k_today_loc:end]:
	tweet_list.append(i)

char_count = 0
first_tweet_list = []

tweet_word = word_tokenize(' '.join(tweet_list))

for i in tweet_word:
	char_count += len(i)
	first_tweet_list.append(i)
	tweet_word = tweet_word[1:]
	if char_count > 200:
		char_count = 0
		break

first_tweet =  ' '.join(first_tweet_list)
first_tweet = first_tweet.replace(" .", ".")
first_tweet = first_tweet.replace(" ,", ",")
first_tweet = first_tweet.replace(" :", ":")
first_tweet = first_tweet.replace(" ;", ";")
first_tweet = first_tweet.replace(" !", "!")
first_tweet = first_tweet.replace(" ?", "?")
api.update_status(status=first_tweet)

print('First Tweet is out. Pausing for a moment...')

time.sleep(10)

status_current =  api.home_timeline(count=1)

for tweet in status_current:
	status_current_id = tweet.id

tweet_sub = []
tweet_sub_str = ''


for i in tweet_word:
	char_count += len(i)
	tweet_sub.append(i)
	tweet_word = tweet_word[1:]
	if char_count > 200:
		tweet_sub_str = ' '.join(tweet_sub)
		tweet_sub_str = tweet_sub_str.replace(" .", ".")
		tweet_sub_str = tweet_sub_str.replace(" ,", ",")
		tweet_sub_str = tweet_sub_str.replace(" :", ":")
		tweet_sub_str = tweet_sub_str.replace(" ;", ";")
		tweet_sub_str = tweet_sub_str.replace(" !", "!")
		tweet_sub_str = tweet_sub_str.replace(" ?", "?")
		api.update_status(status=tweet_sub_str,in_reply_to_status_id=status_current_id)
		tweet_sub = []
		tweet_sub_str = ''
		char_count = 0
		time.sleep(600)
		#Need to grab most current tweet again
		status_current =  api.home_timeline(count=1)
		for tweet in status_current:
			status_current_id = tweet.id


tweet_sub_str = ' '.join(tweet_sub)
tweet_sub_str = tweet_sub_str.replace(" .", ".")
tweet_sub_str = tweet_sub_str.replace(" ,", ",")
tweet_sub_str = tweet_sub_str.replace(" :", ":")
tweet_sub_str = tweet_sub_str.replace(" ;", ";")
tweet_sub_str = tweet_sub_str.replace(" !", "!")
tweet_sub_str = tweet_sub_str.replace(" ?", "?")

api.update_status(status=tweet_sub_str,in_reply_to_status_id=status_current_id)





tweet = ' '.join(tweet_list)
print(tweet)

#tweet_short = []
#if len(tweet) > 270:
#	for i in tweet_list:
#		tweet_short.append(tweet_list[tweet_list.index(i)])
#		tweet = ' '.join(tweet_short)
#		if len(tweet) < 280:
			#api.update_status(tweet)
#			print(tweet)
#		print("length error")
#		tweet_short = []
		#current_status = api.get_user()
		
	

#public_tweets = api.home_timeline()
#for tweet in public_tweets:
#	print tweet.text

