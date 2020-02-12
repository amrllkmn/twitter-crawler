#Twitter Web-crawler (for the Web Science coursework)
#Name: Amirul Lokman Jamaludin
#GUID: 2259783j

from tweepy import OAuthHandler, Stream, StreamListener
import tokens as t

consumer_token = t.consumer_key
consumer_secret = t.consumer_secret

access_token = t.access_token
access_secret = t.access_token_secret

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_status(self, status):
        #Testing to print a number of tweets
        i = 0
        while(i<5):
            print(status.text)
            i+=1
        return False

    def on_error(self,status_code):
        if status_code == 420:
            return False

if __name__ == '__main__':
    print("It's streaming...\n")
    listener = StdOutListener()
    auth = OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    stream = Stream(auth, listener)
    stream.filter(track=['banana'], is_async=True)    
# Trying to store it as a JSON file
