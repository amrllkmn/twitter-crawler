import data_silo as d
import imports as im

stop_words = set(im.stopwords.words('english'))
stop_words.add('https')
#remove stop words
def removeStopWords(text):
    words = []
    tokens = im.word_tokenize(text)
    for word in tokens:
        if word.lower() not in stop_words and word.isalnum():
            words.append(word.lower())
    return ' '.join(word for word in words)

def get_top_features_cluster(tf_idf_array, prediction, n_feats):
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


print("getting collections ...") #obtain from mongodb
filtered = d.filtered
rest_filtered = d.rest_filtered

print("creating dataframes...")
df_filtered = im.pd.DataFrame(list(filtered))
df_rest = im.pd.DataFrame(list(rest_filtered))

print("removing stopwords...")
# combine both dataframes
df_major = im.pd.concat([df_filtered,df_rest])

df_test = df_major

df_test['text'] = df_test['text'].apply(lambda x:removeStopWords(x))

data = df_test['text']


print("vectorising the words to be used for clustering...")
#Calculating the importance of words in each data using TF-IDF
tf_idf_vectorizor = im.TfidfVectorizer(stop_words = 'english',#tokenizer = tokenize_and_stem,
                             max_features = 7000)
tf_idf = tf_idf_vectorizor.fit_transform(data)
tf_idf_norm = im.normalize(tf_idf)
tf_idf_array = tf_idf_norm.toarray()

print("clustering....")
sklearn_pca = im.PCA(n_components = 2)
Y_sklearn = sklearn_pca.fit_transform(tf_idf_array)
kmeans = im.KMeans(n_clusters=3, max_iter=600, algorithm = 'auto')
fitted = kmeans.fit(Y_sklearn)
prediction = kmeans.predict(Y_sklearn)

print("Listing top words in each cluster...")
dfs = get_top_features_cluster(tf_idf_array, prediction, 15)
for i in dfs:
    print(i)
    print('\n')
"""
number_clusters = range(1, 7)

kmeans = [im.KMeans(n_clusters=i, max_iter = 600) for i in number_clusters]
kmeans

score = [kmeans[i].fit(Y_sklearn).score(Y_sklearn) for i in range(len(kmeans))]
score

im.plt.plot(number_clusters, score)
im.plt.xlabel('Number of Clusters')
im.plt.ylabel('Score')
im.plt.title('Elbow Method')
im.plt.show()

print("plotting...")
im.plt.scatter(Y_sklearn[:, 0], Y_sklearn[:, 1], c=prediction, s=50, cmap='viridis')

centers = fitted.cluster_centers_
im.plt.scatter(centers[:, 0], centers[:, 1],c='black', s=300, alpha=0.6)
im.plt.show()
"""
