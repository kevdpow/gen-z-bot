from asyncore import read
import tweepy
import time
import redis
import os
from pprint import pprint
import random
from generate_nouns import get_nouns
import datetime

date_pattern = '%Y-%m-%d %H:%M:%S.%f'

INTERVAL = 60 * 30

# Authenticate to Twitter

creds = {"consumer_key": os.environ.get("TWITTER_API_KEY"),
         "consumer_secret": os.environ.get("TWITTER_API_SECRET"),
         "access_token": os.environ.get("TWITTER_ACCESS_TOKEN"),
         "access_token_secret": os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"), }

client = tweepy.Client(
    **creds
)


def get_used_nouns():
    r = redis.from_url(os.environ.get("REDIS_URL"))
    usedNouns = r.lrange('used_nouns', 0, -1)
    start = r.get("start")
    if start:
        startObj = datetime.datetime.strptime(
            start.decode('utf-8'), date_pattern)
        endObj = startObj + datetime.timedelta(days=30)
        if datetime.datetime.now() > endObj:
            r.delete("used_nouns")
            r.set("start", str(datetime.datetime.now()))
            return []
    elif not start:
        r.set("start", str(datetime.datetime.now()))
    if not usedNouns:
        return []
    return [n.decode("utf-8") for n in usedNouns]


def write_used_noun(noun):
    r = redis.from_url(os.environ.get("REDIS_URL"))
    p = r.lpush("used_nouns", noun)
    return p


def send_genz_tweet():
    usedNouns = get_used_nouns()
    availableNouns = get_nouns()
    print(usedNouns)
    if len(availableNouns):
        nouns = [noun for noun in availableNouns if noun
                 not in usedNouns]
        noun = random.choice(nouns)
        write_used_noun(noun)
    else:
        nouns = usedNouns
        noun = random.choice(nouns)
    tweet = "does gen z know about {}".format(noun)
    client.create_tweet(text=tweet)


while True:
    send_genz_tweet()
    time.sleep(INTERVAL)
