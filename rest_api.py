from imports import Cursor, OAuthHandler, API
import tokens as t
import data_silo as d
import pymongo
import json
import datetime

consumer_token = t.consumer_key
consumer_secret = t.consumer_secret

access_token = t.access_token
access_secret = t.access_token_secret

def REST_keyword_search(keywords,buf,api):
    until = datetime.date.today()
    since = until - datetime.timedelta(days=7)
    print("Searching for tweets with the given keywords...")
    for i in range(len(keywords)):
        buffer = []
        count = 0
        for status in Cursor(api.search,q=keywords[i], lang="en",since=since.strftime("%Y-%m-%d"), until=until.strftime("%Y-%m-%d")).items(200):
            buffer.append(status._json)
            count+=1
        buf+=buffer
        print("Finished searching for: "+keywords[i]+".")

    print("Search complete.")


def REST_users_search(top_users,buf,api):
    print("Searching for tweets from the given usernames...")
    for i in range(len(top_users)):
        buffer = []
        for status in Cursor(api.user_timeline, screen_name=top_users[i], count="200").items(200):
            buffer.append(status._json)
        buf+=buffer
        print("Tweets from @"+top_users[i]+" is complete.")

    print("Search complete.")
"""    
#From the filtered tweets, it would seem that the topics are mainly:

keywords = ["pandemic","quarantine", "#coronavirus", "#COVID-19", "lockdown", "self-isolation"]

#As for the power users, it can be obtained by:

topUsers = d.getMostRetweetedNames("tweets")

auth = OAuthHandler(consumer_token,consumer_secret)
auth.set_access_token(access_token,access_secret)
    
api = API(auth, wait_on_rate_limit=True)
buffer = []

REST_keyword_search(keywords,buffer,api)

REST_users_search(topUsers,buffer,api)

print("Saving to file: rest_api.json...")
with open("rest_api.json","w", encoding="utf-8") as f:
    json.dump(buffer,f,indent=4)
    print("Save complete.")
"""



