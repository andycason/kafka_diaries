# Twitter Bot @Franz_K_Diaries
Twitterbot tweets Franz Kafka's diary entry for the day.

This twitter bot pulls from a text file of diary entries of Franz Kafka and posts them to twitter.

First, it constructs the string of today's date.
Searches the corpus of Kafka's diary entries that has been tokenized into sentences 
and finds the first sentence of the entry and the last sentence of the entry. Then these 
sentences are then pulled and word tokenized for breaking up into tweets. Finally, tweets all parts
of the entry every ten minutes in a threaded format.

This bot also scrolls tweets written in English that mentions Franz Kafka's full name and favorites them.

These scripts are hosted on a RaspberryPi and scheduled to run via crontab.
