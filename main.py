import imports
import streaming
import tokens

if __name__ == '__main__':
    consumer_token  = tokens.consumer_key
    consumer_secret = tokens.consumer_secret
    access_token    = tokens.access_token
    access_secret   = tokens.access_token_secret

    listener = streaming.StdOutListener(30)
    auth     = streaming.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    stream = streaming.Stream(auth, listener)
    stream.filter(track=["I"], locations=[-124.7771694, 24.520833, -66.947028, 49.384472], languages=["en"], is_async=True)

