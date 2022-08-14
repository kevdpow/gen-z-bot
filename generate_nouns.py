import os
import requests
import random
import json
import re
from pprint import pprint

with open("exceptions.txt", mode="r", encoding="utf-8") as outfile:
    noun_exceptions = [n.replace("\n", "") for n in outfile.readlines()]


def normalize_name(name):
    suffix = ""
    suffixes = ["Jr$", "Sr$", "I$", "II$", "III$", "IV$", "V$", "VI$"]
    find = re.search("| ".join(suffixes), name)
    if find:
        suffix = find.group()
    name_split = name.split(",")
    name_split = [n.replace(suffix, "").strip() for n in name_split]
    name_split = [suffix.strip(), *name_split]
    normalized_name = " ".join(name_split[::-1]).strip()
    return normalized_name


def normalize_noun(noun):
    p_exp = "\s\(.+\)\s|\s\(.+\)|\(.+\)\s|\(.+\)"
    find_parentheses = re.findall(p_exp, noun)
    if find_parentheses:
        noun_split = noun.split(find_parentheses[0])
        noun = " ".join(noun_split)
    noun = noun.strip()
    noun = noun.lower()
    for e in noun_exceptions:
        if e in noun:
            return ""
    if noun == "millennial generation":
        noun = "the millennial generation"
    return noun


def get_nouns():
    topics = ["arts", "home", "science", "us", "world"]
    facets = ["des_facet", "per_facet"]
    topic = random.choice(topics)

    url = "https://api.nytimes.com/svc/topstories/v2/{}.json".format(topic)
    querystring = {"api-key": os.environ.get("NYTIMES_KEY")}
    payload = ""
    response = requests.request("GET", url, data=payload, params=querystring)
    if response.status_code == 200:
        obj = json.loads(response.text)
        results = obj["results"]
        nouns = []
        for r in results:
            facet_keys = [key for key in r.keys() if key in facets]
            for key in facet_keys:
                if key == "per_facet" and r["per_facet"]:
                    normalized_names = [normalize_name(
                        n) for n in r["per_facet"]]
                    nouns = [*normalized_names, *nouns]
                else:
                    nouns = [normalize_noun(n) for n in [
                        *nouns, *r[key]] if normalize_noun(n)]
        nouns = list(set(nouns))
        return nouns
    else:
        return []


get_nouns()
