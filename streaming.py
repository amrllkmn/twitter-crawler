#Twitter Web-crawler (for the Web Science coursework)
#Name: Amirul Lokman Jamaludin
#GUID: 2259783j

from tweepy import OAuthHandler, Stream, StreamListener
import tokens as t
import json as j

consumer_token = t.consumer_key
consumer_secret = t.consumer_secret

access_token = t.access_token
access_secret = t.access_token_secret

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    The listener collects exactly 5 tweets.
    """
    def __init__(self, limit):
        self.d = {} # empty dictionary to store data
        self.limit = limit
        self.file = open("twitter_data.json","w",encoding="utf-8")
        self.count = 0

    def on_data(self,data):
        if self.count < self.limit:
            self.d[self.count] = data 
            self.count+=1
            print(self.count)
            return True
        else:
            j.dump(self.d,self.file,indent=4) #Once done, just dump data in a json file before finishing
            self.file.close()
            return False

        
    
    def on_error(self,status):
        print(status)

if __name__ == '__main__':
    print("It's streaming...\n")
    listener = StdOutListener(5)
    auth = OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    stream = Stream(auth, listener)
    stream.filter(track=['Tesla'], is_async=True)
    