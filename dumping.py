import json
import data_silo as d
import os
def dumping(filename):
    if os.path.isfile(filename) and os.path.getsize !=0:
        with open(filename,"r", encoding="utf-8") as f:
                print("Begin insertion to database...")
                data = json.load(f)
                d.db[filename[:-5]].insert_many(data)
                print("Insertion complete.")
    else:
        print("File is empty or doesn't exist")