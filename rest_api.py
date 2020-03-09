from tweepy import OAuthHandler, API, Cursor
import tokens as t
import data_silo as d
consumer_token = t.consumer_key
consumer_secret = t.consumer_secret

access_token = t.access_token
access_secret = t.access_token_secret

if __name__ == '__main__':

    auth = OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api  = API(auth, wait_on_rate_limit=True)

    database = d.db.REST_sample

    cursor = Cursor(api.search,q="COVID-19", until="", count="100").items(1000)

    for items in cursor:
        all_data = items._json
        try:
            database.insert_one(all_data)
        except Exception as err:
            print(err)