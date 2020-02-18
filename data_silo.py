import pymongo


client = pymongo.MongoClient('mongodb+srv://amrllkmn:twtcrawler2011@twtcrawler-ziohm.mongodb.net/test?retryWrites=true&w=majority')
db = client.test

result = db.count_doc.insert_one({'x':1})

print(result)