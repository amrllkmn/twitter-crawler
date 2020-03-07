import pymongo
import dns

client = pymongo.MongoClient('mongodb+srv://amrllkmn:TwitterWebCrawling@database-pkr2p.mongodb.net/test?retryWrites=true&w=majority')
db = client.tweets