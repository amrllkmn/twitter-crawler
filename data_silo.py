import imports as im
import time

client = im.pymongo.MongoClient('mongodb+srv://amrllkmn:TwitterWebCrawling@database-pkr2p.mongodb.net/test?retryWrites=true&w=majority')
db = client.tweets

def getCollection(collectionName): #Returns collection
    try:
        collection = db[collectionName]
    except Exception as e:
        print(e)
    
    return collection

def getMostRetweetedNames(collectionName): #Returns 15 most retweeted users
    """Returns most retweeted tweets"""
    cursor = db[collectionName+"_filtered"].find({"user.verified":True, "retweet_count":{"$gt":1000}}).sort([('retweet_count',-1)]).limit(15)
    cursor = [items["user"]["screen_name"] for items in cursor]
    
    return cursor

def getMostLiked(collectionName): #Returns most liked tweet
    """ Returns most liked tweets """
    cursor = db[collectionName].find().sort([('favorite_count',-1)]).limit(1)
    cursor = list(cursor)

    return cursor[0]