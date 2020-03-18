import data_silo as d
import time
#collection = d.db['REST_sample'].find({'retweet_count': {'$t':1000}})

collection = d.getCollection("bad")

x = time.time()
for docs in collection.find():
    try:
        if docs["retweeted_status"]["truncated"] == True:
            d.db.rest_filtered.insert_one({"id":docs["retweeted_status"]["id"], "created_at":docs["retweeted_status"]["created_at"], "text":docs["retweeted_status"]["extended_tweet"]["full_text"], "user":docs["retweeted_status"]["user"], "retweet_count":docs["retweeted_status"]["retweet_count"]})
        else:
            d.db.rest_filtered.insert_one({"id":docs["retweeted_status"]["id"], "created_at":docs["retweeted_status"]["created_at"], "text":docs["retweeted_status"]["text"], "user":docs["retweeted_status"]["user"],"retweet_count":docs["retweeted_status"]["retweet_count"]})
    except KeyError:
        if docs["truncated"] == True:
            d.db.rest_filtered.insert_one({"id":docs["id"], "created_at":docs["created_at"], "text":docs["extended_tweet"]["full_text"], "user":docs["user"], "retweet_count":docs["retweet_count"]})
        else:
            d.db.rest_filtered.insert_one({"id":docs["id"], "created_at":docs["created_at"], "text":docs["text"], "user":docs["user"],"retweet_count":docs["retweet_count"]})
print(time.time() - x)

