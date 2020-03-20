import imports as im
import tokens as t
import data_silo as d
import pymongo

consumer_token = t.consumer_key
consumer_secret = t.consumer_secret

access_token = t.access_token
access_secret = t.access_token_secret

if __name__ == '__main__':
    #From the filtered tweets, it would seem that
    #the topics are mainly:

    keywords = ["pandemic","quarantine", "#coronavirus", "#COVID-19", "lockdown", "self-isolation"]

    #As for the power users, it can be obtained by:

    topUsers = d.getMostRetweetedNames("filtered") #['MrBeastYT', 'pulte', 'elonmusk', 'BTS_twt', 'samsmith', 'Louis_Tomlinson', 'SethAbramson', 'evanmcmurry', 'maxbrooksauthor', 'EricHaywood']

    auth = im.OAuthHandler(consumer_token,consumer_secret)
    auth.set_access_token(access_token,access_secret)

    api = im.API(auth,wait_on_rate_limit=True)

    master_buf = []
    for i in range(len(keywords)):
        buffer = []
        for status in im.Cursor(api.search,q=keywords[i], lang="en",since="2020-03-12", until="2020-03-19").items(2000):
            buffer.append(status._json)
        master_buf+=buffer
        print(keywords[i]+" is complete.")
    
    for i in range(len(topUsers)):
        buffer = []
        for status in im.Cursor(api.user_timeline, screen_name=topUsers[i], count="200").items(2000):
            buffer.append(status._json)
        master_buf+=buffer
        print(topUsers[i]+" is complete.")
    
    database = d.db.REST_api
    try:
        print("Inserting...")
        database.insert_many(master_buf,ordered=False)
    except pymongo.errors.BulkWriteError as bwe:
        for err in bwe.details["writeErrors"]:
            if int(err['code']) == 11000:
                pass
            else:
                print(err['errmsg'])




