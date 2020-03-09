import data_silo as d

#collection = d.db['REST_sample'].find({'retweet_count': {'$t':1000}})

print(d.getMostRetweeted('REST_sample'))


