import data_silo as d

collection = d.getCollection("REST_sample")

for docs in collection.find():
    try:
        print("RT:" + docs["retweeted_status"]["text"])
    except KeyError:
        print(docs["text"])