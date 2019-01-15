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


if d_format[0] == "0":
	d_format = d_format[1:]

#Opening up the kafka.txt file here

k_raw = open('/home/pi/kafka/kafka.txt', 'rU').read().decode('ascii','ignore')

k_sents = sent_tokenize(k_raw)
	

loc_list = []

for i in range(len(k_sents)):
	if d_format in k_sents[i]:
		loc_list.append(i)

print('Entries for thie date are found here: ' + ' and '.join([str(i) for i in loc_list]))


def findEnd(x):
	#find last sentence
	next = []

	nextmonth = datetime.date.today() + relativedelta.relativedelta(month=1)


	next60days  = []

	for i in range(60):
		next_day = datetime.date.today() + relativedelta.relativedelta(days=i)
		next_day_format = next_day.strftime("%d %B.")
		if next_day_format[0] == "0":
			next_day_format = next_day_format[1:]
		next60days.append(next_day_format)


	next60days = next60days[1:]

	start = int(x+1)
	startplus100 = int(x+100)
	search_range = k_sents[start:startplus100]

	for i in next60days:
		try:
			next.append(search_range.index(i))
		except:
			pass

	end = x + next[0]
	return end


end_loc =[]

for i in loc_list:
	end_loc.append(findEnd(i))
	print('an ending was found here ' + str(findEnd(i)))


def cleanText(string):
	string = string.replace(" .", ".")
	string = string.replace(" ,", ",")
	string = string.replace(" :", ":")
	string = string.replace(" ;", ";")
	string = string.replace(" !", "!")
	string = string.replace(" ?", "?")
	string = string.replace(" )", ")")
	string = string.replace("( ", "(")
	return string




def makeTweet(begin,end):
	#make the tweet

	tweet_list = []

	for i in k_sents[begin:end]:
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
	first_tweet = cleanText(first_tweet)
	api.update_status(status=first_tweet)
	print(first_tweet)
	print('First Tweet is out. Pausing for a moment...')

	time.sleep(60)

	status_current =  api.home_timeline(count=1)

	for tweet in status_current:
		status_current_id = tweet.id

	tweet_sub = []
	tweet_sub_str = ''
	tweet_number = 1

	for i in tweet_word:
		char_count += len(i)
		tweet_sub.append(i)
		tweet_word = tweet_word[1:]
		if char_count > 200:
			tweet_sub_str = ' '.join(tweet_sub)
			tweet_sub_str = cleanText(tweet_sub_str)
			api.update_status(status=tweet_sub_str,in_reply_to_status_id=status_current_id)
			tweet_number += 1
			print("Tweeted tweet number " + str(tweet_number))
			print(tweet_sub_str)
			tweet_sub = []
			tweet_sub_str = ''
			char_count = 0
			time.sleep(300)
			#Need to grab most current tweet again 
			#be sure to comment out api calls to reduce rate limit exhaustion
			status_current =  api.home_timeline(count=1)
			for tweet in status_current:
				status_current_id = tweet.id


	tweet_sub_str = ' '.join(tweet_sub)
	tweet_sub_str = cleanText(tweet_sub_str)

	api.update_status(status=tweet_sub_str,in_reply_to_status_id=status_current_id)
	print ("Tweeted last tweet!")
	print(tweet_sub_str)



for i in range(len(loc_list)):
	makeTweet(loc_list[i],end_loc[i])



