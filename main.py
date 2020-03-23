import imports
import streaming
import tokens
import filtering
import data_silo
import dumping
import rest_api
import clustering
import stats


if __name__ == '__main__':
    consumer_token  = tokens.consumer_key
    consumer_secret = tokens.consumer_secret
    access_token    = tokens.access_token
    access_secret   = tokens.access_token_secret
    keywords = ["the","of", "and", "a","to"] # Change keywords here 
    #Streaming
    listener = streaming.StdOutListener(30)  # Takes in integer as seconds to stream data
    auth     = streaming.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    stream = streaming.Stream(auth, listener)
    stream.filter(track=keywords, locations=[-124.7771694, 24.520833, -66.947028, 49.384472], languages=["en"], is_async=True)

    while listener.isDoneStreaming() is not True:
        continue
    filename = listener.getFilename() #returns file name with .json
    print("Tweets are dumped in file called: "+filename)
    dumping.dumping(filename)
    streaming_collection = filename[:-5] #remove the .json extension
    filtering.filter(streaming_collection) #filters the statuses and store in a database called tweets_filtered
    
    #Obtaining data for REST
    topUsers = data_silo.getMostRetweetedNames(streaming_collection) # get top retweeted users from filtered streaming data
    print("The top retweets from the stream is: "+str(topUsers))
    print("The keywords are: "+ str(keywords))

    #REST API
    api = imports.API(auth, wait_on_rate_limit=True)
    buffer = []
    rest_api.REST_keyword_search(keywords,buffer,api) #Search Twitter with the given keywords
    rest_api.REST_users_search(topUsers,buffer,api)   #Searches the user timeline for the given list of users
    print("Saving to file: rest_tweets.json...")
    with open("rest_tweets.json","w", encoding="utf-8") as f:
        imports.json.dump(buffer,f,indent=4)
        print("Save complete.")
    
    dumping.dumping("rest_tweets.json")
    rest_collection = "rest_tweets.json"[:-5]
    filtering.REST_filter(rest_collection) # The filtered collection will be called "rest_tweets_filtered"

    #Clustering
    print("Getting collections ...") #obtain collection from mongodb
    stream_filtered = data_silo.getCollection("tweets_filtered").find()
    rest_filtered   = data_silo.getCollection("rest_tweets_filtered").find()

    print("creating dataframes...")
    df_filtered = imports.pd.DataFrame(list(stream_filtered))
    df_rest = imports.pd.DataFrame(list(rest_filtered))

    print("removing stopwords...")
    # combining both dataframes
    df_major = imports.pd.concat([df_filtered,df_rest])

    df_major['text'] = df_major['text'].apply(lambda x:clustering.removeStopWords(x))

    data = df_major['text']

    print("vectorising the words to be used for clustering...")
    #Calculating the importance of words in each data using TF-IDF
    tf_idf_vectorizor = imports.TfidfVectorizer(stop_words = 'english',#tokenizer = tokenize_and_stem,
                             max_features = 20000)
    tf_idf            = tf_idf_vectorizor.fit_transform(data)
    tf_idf_norm       = imports.normalize(tf_idf)
    tf_idf_array      = tf_idf_norm.toarray()

    print("clustering....")
    sklearn_pca = imports.PCA(n_components = 2)
    Y_sklearn   = sklearn_pca.fit_transform(tf_idf_array)
    kmeans      = imports.KMeans(n_clusters=3, max_iter=600, algorithm = 'auto')
    fitted      = kmeans.fit(Y_sklearn)
    prediction  = kmeans.predict(Y_sklearn)

    print("Listing top words in each cluster...")
    dfs = clustering.get_top_features_cluster(tf_idf_vectorizor,tf_idf_array, prediction, 15)
    for i in dfs:
        print(i)
        print('\n')

    #From the collection
    #Collections in the database will be called: "rest_tweets_filtered", "tweets_filtered"
    print("Getting mentions for: @realDonaldTrump...")
    mentions = stats.getMentions("rest_tweets_filtered","realDonaldTrump") #Takes in the name of the collection and the intended username
    print(mentions)