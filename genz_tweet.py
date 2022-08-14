from asyncore import read
import tweepy
import time
import os
from pprint import pprint
import random
from generate_nouns import get_nouns

INTERVAL = 60 * 30

# Authenticate to Twitter

creds = {"consumer_key": os.environ.get("TWITTER_API_KEY"),
         "consumer_secret": os.environ.get("TWITTER_API_SECRET"),
         "access_token": os.environ.get("TWITTER_ACCESS_TOKEN"),
         "access_token_secret": os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"), }

client = tweepy.Client(
    **creds
)


# def read_used_nouns():
#     with open("usedNouns.log", mode="r", encoding="utf-8") as outfile:
#         data = [r.replace("\n", "") for r in outfile.readlines()]
#         return data


def write_used_noun(noun):
    str = noun + "\n"
    with open("usedNouns.log", mode="a", encoding='utf-8') as infile:
        infile.write(str)


def send_genz_tweet():
    # usedNouns = read_used_nouns()
    nouns = get_nouns()
    if len(nouns):
        noun = random.choice(nouns)
        tweet = "does gen z know about {}".format(noun)
        client.create_tweet(text=tweet)
    # if len(availableNouns):
    #     nouns = [noun for noun in availableNouns if noun
    #              not in usedNouns]
    #     noun = random.choice(nouns)
    #     write_used_noun(noun)
    # else:
    #     nouns = usedNouns
    #     noun = random.choice(nouns)
    # tweet = "does gen z know about {}".format(noun)
    # client.create_tweet(text=tweet)


send_genz_tweet()

# while True:
#     send_genz_tweet()
#     time.sleep(INTERVAL)
