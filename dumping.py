import json
import data_silo as d
with open("tweets_2.json","r", encoding="utf-8") as f:
    data = json.load(f)
    data = data[:int(len(data)/4)]
    d.db.tweet_dump.insert_many(data)