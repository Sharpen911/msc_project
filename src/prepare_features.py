import pandas as pd
import numpy as np
import math
import pickle

import gensim.models as gs
import nltk.tokenize as tk
import phrase2vec as p2v
from tqdm import tqdm
from os import listdir
import utils

def prepare_feature_vector(tweets, p2v):
    """
    Args:
        tweets: All tweets of a user
        p2v: Phrase2Vec model

    Returns:
        Average vectors for each user

    """
    tweets.dropna(inplace=True)
    user_features = np.zeros(300)
    if len(tweets) == 0:
        return user_features
    tokenizer = tk.TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles=True)
    for tweet in tweets:
        tokens = tokenizer.tokenize(tweet)
        if len(tokens) ==0:
            user_features+=0
        else:
            user_features += np.sum([p2v[x] for x in tokens], axis=0) / len(tokens)

    user_features = user_features / len(tweets)
    return user_features


w2v_path='./pre-trained/GoogleNews-vectors-negative300.bin'
e2v_path = './pre-trained/emoji2vec.bin'

w2v = gs.KeyedVectors.load_word2vec_format(w2v_path, binary=True)
e2v = gs.KeyedVectors.load_word2vec_format(e2v_path, binary=True)


parent_df_path = 'usage_per_user/'
cities = ['joh', 'lon', 'nyc', 'ran']

user_features = pd.DataFrame()

types = ['text', 'emoji', 'both']
# types = ['emoji']

for feature_type in types:
    user_features_all = pd.DataFrame()

    if feature_type == 'text':
        model = p2v.Phrase2Vec(300, w2v, e2v=None)
    elif feature_type == 'emoji':
        model = p2v.Phrase2Vec(300, e2v, e2v=None)
    else:
        model = p2v.Phrase2Vec(300, w2v, e2v=e2v)

    for city in cities:

        user_information = pd.read_csv('user_data/' + city + '.csv', index_col='user_id',usecols=['user_id', 'gender', 'ethnicity'])
        user_demog = user_information.dropna().to_dict('index')

        labeled = user_demog.keys()
        collected = [int(name[:-11]) for name in listdir(utils.tweets_save_dir + city)]

        labeled_users = set.intersection(set(labeled), set(collected))

        num_of_users = len(labeled_users)

        user_features = pd.DataFrame(np.zeros(shape=(num_of_users, 300)), columns=range(300))

        for enum, user_id in enumerate(tqdm(labeled_users)):
            try:
                file_path = 'collected_tweets/' + city + '/' + str(user_id) + '_tweets.csv'
                user_tweets = pd.read_csv(file_path, lineterminator='\n', usecols=['text'])

                feature = prepare_feature_vector(user_tweets.text, model)

                series = pd.Series(feature)
                user_features.at[enum] = series

                user_features.at[enum, 'gender'] = user_demog[user_id]['gender']
                user_features.at[enum, 'ethnicity'] = user_demog[user_id]['ethnicity']

            except Exception as e:

                print(e)
                print(user_id)


        user_features_all = user_features_all.append(user_features)

    save_path = 'features/' + feature_type + '_.pkl'
    user_features_all.to_pickle(save_path)
    print('Save the {} features into: {}'.format(feature_type, save_path))









