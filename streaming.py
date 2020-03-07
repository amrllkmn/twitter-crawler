#Twitter Web-crawler (for the Web Science coursework)
#Name: Amirul Lokman Jamaludin
#GUID: 2259783j

from tweepy import OAuthHandler, Stream, StreamListener
import tokens as t
import json as j
import data_silo as d

consumer_token = t.consumer_key
consumer_secret = t.consumer_secret

access_token = t.access_token
access_secret = t.access_token_secret

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    The listener collects as much tweets as possible
    """
    def __init__(self):
        self.count = 0

    def on_data(self,data):
        #try:
            if self.count < 5:
                j_data = j.loads(data)
                d.db.altered_carbon.insert_one(j_data)
                self.count +=1
                print(self.count)
                return True
            else:
                return False
        #except Exception as e:
           # print(e)
           # return False

    def on_error(self,status):
        print(status)

if __name__ == '__main__':
    print("It's streaming...\n")
    listener = StdOutListener()
    auth = OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    stream = Stream(auth, listener)
    stream.filter(track=['Altered Carbon'], is_async=True)
    