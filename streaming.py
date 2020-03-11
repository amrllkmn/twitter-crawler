#Twitter Web-crawler (for the Web Science coursework)
#Name: Amirul Lokman Jamaludin
#GUID: 2259783j

from tweepy import OAuthHandler, Stream, StreamListener
import tokens as t
import json as j
import data_silo as d
import time as tm

consumer_token = t.consumer_key
consumer_secret = t.consumer_secret

access_token = t.access_token
access_secret = t.access_token_secret

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    The listener collects as much tweets as possible
    """
    def __init__(self,timelimit=60):
        self.start = tm.time()
        self.limit = timelimit
        super(StdOutListener,self).__init__()

    def on_data(self,data):
        print(self.get_time())
        try:
            if(tm.time() - self.start) < self.limit:
                d.db.castlevania_five_min.insert_one(j.loads(data)) #add document into collection
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def on_error(self,status):
        print(status)
    
    def get_time(self):
        return int(tm.time() - self.start)

if __name__ == '__main__':
    print("It's streaming...\n")
    listener = StdOutListener(30)
    auth = OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    stream = Stream(auth, listener)
    stream.filter(track=['Castlevania'], is_async=True)
    
    