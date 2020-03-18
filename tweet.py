import json
import data_silo as d
with open("tweets.json","r") as f:
    data = json.load(f)
    d.db.test_write.insert_many(data)