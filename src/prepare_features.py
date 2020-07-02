import pandas as pd
import numpy as np
import math
import gensim.models as gs
import pickle as pk
import pickle
import nltk.tokenize as tk
import phrase2vec as p2v
from tqdm import tqdm

def prepare_feature_vector(tweets, p2v):
    """
    Args:
        tweets: All tweets of a user
        p2v: Phrase2Vec model

    Returns:
        Average vectors for each user

    """
    user_features = np.zeros(300)
    tokenizer = tk.TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles=True)
    for tweet in tweets:
        tokens = tokenizer.tokenize(tweet)
        user_features += np.sum([p2v[x] for x in tokens], axis=0) / len(tokens)

    user_features = user_features / len(tweets)
    return user_features


# w2v_path='./pre-trained/GoogleNews-vectors-negative300.bin'
e2v_path = './pre-trained/emoji2vec.bin'

# w2v = gs.KeyedVectors.load_word2vec_format(w2v_path, binary=True)
e2v = gs.KeyedVectors.load_word2vec_format(e2v_path, binary=True)


parent_df_path = 'usage_per_user/'
cities = ['joh', 'lon', 'nyc', 'ran']

user_features = pd.DataFrame()

# types = ['text', 'emoji', 'both']
types = ['emoji']
for feature_type in tqdm(types):
    if feature_type == 'text':
        model = p2v.Phrase2Vec(300, w2v, e2v=None)
    elif feature_type == 'emoji':
        model = p2v.Phrase2Vec(300, e2v, e2v=None)
    else:
        model = p2v.Phrase2Vec(300, w2v, e2v=e2v)

    for city in cities:

        with open(parent_df_path + city +'_df.pkl', 'rb') as f:
            per_usage = pickle.load(f)
            per_usage.dropna(inplace=True)
            per_usage.drop(labels=per_usage[per_usage.total_tweets.eq(0)].index, inplace=True)
            per_usage.drop(labels=per_usage[per_usage.ethnicity.eq(5)].index, inplace=True)

        for user_id in per_usage.user_id:
            file_path = 'collected_tweets/' + city + '/' + str(int(user_id))+'_tweets.csv'
            user_tweets = pd.read_csv(file_path, usecols=['text'])

            feature = prepare_feature_vector(user_tweets.text, model)

            series = pd.Series(feature)
            user_features = user_features.append(series, ignore_index=True)
            user_features['user_id'] = user_id
    save_path = 'features/' + feature_type + '_.pkl'
    user_features.to_pickle(save_path)










