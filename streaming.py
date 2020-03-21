#Twitter Web-crawler (for the Web Science coursework)
#Name: Amirul Lokman Jamaludin
#GUID: 2259783j

#import imports as im
import tokens as t
import json as j
import data_silo as d
import time
from tweepy import OAuthHandler, Stream, StreamListener,API, Cursor
consumer_token = t.consumer_key
consumer_secret = t.consumer_secret

access_token = t.access_token
access_secret = t.access_token_secret

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    The listener collects as much tweets as possible given the time limit in seconds
    """
    def __init__(self,timelimit=60):
        self.start = time.time()
        self.limit = timelimit
        self.file = open("tweets.json","w", encoding="utf-8")
        self.list = []
        self.buf_list = []
        print(str(self.limit)+" seconds to stream")
        super(StdOutListener,self).__init__()

    def on_data(self,data):
        #Stores data in database, then returns true to continue stream, else disconnects stream
        try:
            
            if(time.time() - self.start) < self.limit:
                tweet = j.loads(data)
                self.list.append(tweet) #add tweet to list
                if len(self.list) > 1000:
                    self.buf_list+=self.list #add list to buffer
                    self.list = []
                return True
            else:
                print("Streming complete, got "+ str(len(self.buf_list))+" tweets. Dumping into file...")
                j.dump(self.buf_list,self.file, indent=4) #store in json file
                self.file.close()
                print("Dumping complete")
                return False
        except Exception as e:
            print("Streaming failed: "+e)
            self.file.close()
            return False

    def on_error(self,status):

        print("Streaming failed: "+status)
    
#
#if __name__ == '__main__':
#    print("It's streaming...\n")
#    listener = StdOutListener(10)
#    auth = OAuthHandler(consumer_token, consumer_secret)
#    auth.set_access_token(access_token, access_secret)

#    stream = Stream(auth, listener)
#    stream.filter(track=['the','of', 'and', 'a', 'to'], locations=[-124.7771694, 24.520833, -66.947028, 49.384472], languages=["en"], is_async=True)
    
    