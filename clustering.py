import data_silo as d
import imports as im

stop_words = set(im.stopwords.words('english'))
stop_words.add('https')
#remove stop words
def removeStopWords(text): #Returns a sentence without stop words
    words = []
    tokens = im.word_tokenize(text)
    for word in tokens:
        if word.lower() not in stop_words and word.isalnum():
            words.append(word.lower())
    return ' '.join(word for word in words)

def get_top_features_cluster(tf_idf_vectorizor,tf_idf_array, prediction, n_feats): #Returns list of top words for cluster
    labels = im.np.unique(prediction)
    dfs = []
    for label in labels:
        id_temp = im.np.where(prediction==label) # indices for each cluster
        x_means = im.np.mean(tf_idf_array[id_temp], axis = 0) # returns average score across cluster
        sorted_means = im.np.argsort(x_means)[::-1][:n_feats] # indices with top 20 scores
        features = tf_idf_vectorizor.get_feature_names()
        best_features = [(features[i], x_means[i]) for i in sorted_means]
        df = im.pd.DataFrame(best_features, columns = ['features', 'score'])
        dfs.append(df)
    return dfs

