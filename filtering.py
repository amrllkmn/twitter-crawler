import data_silo as d
import imports as im
#collection = d.db['REST_sample'].find({'retweet_count': {'$t':1000}})
def filter():
    x = im.time.time()
    collection = d.getCollection("tweet_dump")

    array = []
    for docs in collection.find():
        try:
            if docs["retweeted_status"]["truncated"] == True:
                array.append({"id":docs["retweeted_status"]["id"], "created_at":docs["retweeted_status"]["created_at"], "text":docs["retweeted_status"]["extended_tweet"]["full_text"], "user":docs["retweeted_status"]["user"], "retweet_count":docs["retweeted_status"]["retweet_count"]})
            else:
                array.append({"id":docs["retweeted_status"]["id"], "created_at":docs["retweeted_status"]["created_at"], "text":docs["retweeted_status"]["text"], "user":docs["retweeted_status"]["user"],"retweet_count":docs["retweeted_status"]["retweet_count"]})
        except KeyError:
            if docs["truncated"] == True:
                array.append({"id":docs["id"], "created_at":docs["created_at"], "text":docs["extended_tweet"]["full_text"], "user":docs["user"], "retweet_count":docs["retweet_count"]})
            else:
                array.append({"id":docs["id"], "created_at":docs["created_at"], "text":docs["text"], "user":docs["user"],"retweet_count":docs["retweet_count"]})
    

    database = d.db.filtered
    database.create_index("id",unique=True)
    try:
        print("Inserting...")
        database.insert_many(array,ordered=False)
    except im.pymongo.errors.BulkWriteError as bwe:
        for err in bwe.details["writeErrors"]:
            if int(err['code']) == 11000:
                pass
            else:
                print(err['errmsg'])
    finally:
        print(im.time.time() - x)