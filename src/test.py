# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# import numpy as np
# import phrase2vec as p2v
# import gensim.models as gs
# import nltk.tokenize as tk
# import pandas as pd
#



#
# import pandas as pd
# import numpy as np
# import math
# import pickle
#
# import gensim.models as gs
# import nltk.tokenize as tk
# import phrase2vec as p2v
# from tqdm import tqdm
# from os import listdir
# import utils
#
# def prepare_feature_vector(tweets, p2v):
#     """
#     Args:
#         tweets: All tweets of a user
#         p2v: Phrase2Vec model
#
#     Returns:
#         Average vectors for each user
#
#     """
#
#     tweets.dropna(inplace = True)
#     user_features = np.zeros(300)
#     if len(tweets) == 0:
#         return user_features
#     tokenizer = tk.TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles=True)
#     for tweet in tweets:
#
#         tokens = tokenizer.tokenize(tweet)
#         if len(tokens) ==0:
#             user_features+=0
#         else:
#             user_features += np.sum([p2v[x] for x in tokens], axis=0) / len(tokens)
#
#     user_features = user_features / len(tweets)
#     return user_features
#
# user_tweets = pd.read_csv('collected_tweets/joh/501711341_tweets.csv', lineterminator='\n', usecols=['text'])
# # print(user_tweets.text.dropna())
# print(user_tweets[user_tweets.isnull().any(axis=1)])
# w2v_path='./pre-trained/GoogleNews-vectors-negative300.bin'
# e2v_path = './pre-trained/emoji2vec.bin'
#
# w2v = gs.KeyedVectors.load_word2vec_format(w2v_path, binary=True)
# e2v = gs.KeyedVectors.load_word2vec_format(e2v_path, binary=True)
#
# model = p2v.Phrase2Vec(300, w2v, e2v=e2v)
# feature = prepare_feature_vector(user_tweets.text, model)
#
# series = pd.Series(feature)
# print(series)


import sys
import time
import string
import random
# from lxml import etree
#
# import xml.etree.ElementTree as xml
# import pandas as pd
# from os import listdir
# import xml.dom.minidom as minidom
# import utils
# # , 'lon', 'nyc', 'ran'
# cities = ['joh']
# for city in cities:
#     user_information = pd.read_csv('user_data/' + city + '.csv', index_col='user_id',usecols=['user_id', 'gender', 'ethnicity'])
#     user_demog = user_information.dropna().to_dict('index')
#
#     labeled = user_demog.keys()
#     collected = [int(name[:-11]) for name in listdir(utils.tweets_save_dir + city)]
#     labeled_users = set.intersection(set(labeled), set(collected))
#
#     en_txt = []
#
#     for user_id in labeled_users:
#
#
#
#         author = etree.Element('author')
#
#         documents = etree.SubElement(author, 'documents')
#
#
#         file_path = 'collected_tweets/' + city + '/' + str(user_id) + '_tweets.csv'
#         user_tweets = pd.read_csv(file_path, lineterminator='\n', usecols=['text'])
#
#         if len(user_tweets.text) <=1:
#
#             document = etree.SubElement(documents, 'document')
#             document.text = "this user have no tweets"
#
#         else:
#             i=1
#             for tweet in user_tweets.text:
#                 if i ==100:
#                     break
#
#                 tweet = etree.CDATA(tweet.replace("\r","").replace("\n",""))
#                 document = etree.SubElement(documents, 'document')
#                 document.text = tweet
#                 i += 1
#
#         user_with_label = str(user_id) + ':::' + user_demog[user_id]['gender']
#         en_txt.append(user_with_label)
#
#
#
#         dataxml = etree.tostring(author, pretty_print=True, encoding="UTF-8", method="xml", xml_declaration=False, standalone=None)
#         # print(type(dataxml.decode()))
#         with open('D:/Pan/train/en/text/' + str(user_id) + '.xml', 'w', encoding='utf-8') as f:
#             f.write(dataxml.decode())
#
#
#
#
#
#     print(en_txt)
#     with open("D:/Pan/train/en/text/truth.txt", 'w') as output:
#         for row in en_txt:
#             output.write(str(row) + '\n')
import pandas as pd
import numpy as np
import math
import pickle
from sklearn.model_selection import train_test_split


import nltk.tokenize as tk
import phrase2vec as p2v
from tqdm import tqdm
from os import listdir
import utils
# , 'lon', 'nyc', 'ran'
cities = ['joh','lon', 'nyc', 'ran']

build_gender = []
build_eth = []
# for city in cities:
#
#     user_information = pd.read_csv('user_data/' + city + '.csv', index_col='user_id',
#                                    usecols=['user_id', 'gender', 'ethnicity'])
#
#     user_information["ethnicity"].replace({"other": None,"asian":"latino","hispanic":"latino"}, inplace=True)
#     user_demog = user_information.dropna().to_dict('index')
#
#     labeled = user_demog.keys()
#     collected = [int(name[:-11]) for name in listdir(utils.tweets_save_dir + city)]
#
#     labeled_users = set.intersection(set(labeled), set(collected))
#
#     num_of_users = len(labeled_users)
#
#
#
#     for enum, user_id in enumerate(tqdm(labeled_users)):
#         try:
#             file_path = 'collected_tweets/' + city + '/' + str(user_id) + '_tweets.csv'
#             user_names = pd.read_csv(file_path, lineterminator='\n', usecols=['user_name', 'user_screen_name'])
#
#             if len(user_names)>0:
#                 names_eth = str(user_names.user_name[0]) + '\t' + str(user_names.user_screen_name[0]) + '\t' + 'description' + '\t' + str(user_demog[user_id]['ethnicity'])
#                 names_gender = str(user_names.user_name[0]) + '\t' + str(user_names.user_screen_name[0]) + '\t' + 'description' + '\t' + str(user_demog[user_id]['gender'])
#             else:
#                 names_eth = 'invalid user_name' + '\t' + 'invalid screen_name' + '\t' + 'description' + '\t' + str(user_demog[user_id]['ethnicity'])
#                 names_gender = 'invalid user_name' + '\t' + 'invalid screen_name' + '\t' + 'description' + '\t' + str(user_demog[user_id]['gender'])
#
#
#
#             build_eth.append(names_eth+'\n')
#             build_gender.append(names_gender+'\n')
#
#         except Exception as e:
#
#             print(e)
#             print(user_id)
#
# with open(r'D:\temp_data\tf_preprocess\wlb_build.txt','w', encoding='utf-8') as f:
#     f.write(''.join(build_eth))
#
#
# with open(r'D:\temp_data\tf_preprocess\mf_build.txt','w', encoding='utf-8') as f:
#     f.write(''.join(build_gender))


# # for ethnicity
# df_eth = pd.read_csv(r'D:\temp_data\tf_preprocess\wlb_build.txt',encoding='utf-8',delimiter='\t',names=['name','screen_name','description','label'])
#
#
# X_train_eth, X_test_eth, y_train_eth, y_test_eth = train_test_split(df_eth.drop(columns = ['description','label']),df_eth['label'],test_size=0.2, random_state=43)
#
#
# train_names = X_train_eth.values.tolist()
# train_labels = y_train_eth.values.tolist()
#
# test_names = X_test_eth.values.tolist()
# test_labels = y_test_eth.values.tolist()
#
#
#
# with open(r'D:\temp_data\tf_preprocess\wlb.train.txt', 'a',encoding='utf-8') as f:
#     for name,label in zip(train_names,train_labels):
#
#         f.write(label +'\t'+name[-1]+'\n')
#
#
# with open(r'D:\temp_data\tf_preprocess\wlb.dev.txt','a',encoding='utf-8') as f:
#     for name,label in zip(test_names,test_labels):
#
#         f.write(label +'\t'+name[-1]+'\n')
#
# with open(r'D:\temp_data\tf_preprocess\wlb.test.txt','a',encoding='utf-8') as f:
#     for name,label in zip(test_names,test_labels):
#
#         f.write(label +'\t'+name[-1]+'\n')




# for gender

df_gender = pd.read_csv(r'D:\temp_data\tf_preprocess\mf_build.txt',encoding='utf-8',delimiter='\t',names=['name','screen_name','description','label'])


X_train_gender, X_test_gender, y_train_gender, y_test_gender = train_test_split(df_gender.drop(columns = ['description','label']),df_gender['label'],test_size=0.2, random_state=43)


train_names = X_train_gender.values.tolist()
train_labels = y_train_gender.values.tolist()

test_names = X_test_gender.values.tolist()
test_labels = y_test_gender.values.tolist()



with open(r'D:\temp_data\tf_preprocess\mf.train.txt', 'a',encoding='utf-8') as f:
    for name,label in zip(train_names,train_labels):

        f.write(label +'\t'+name[-1]+'\n')


with open(r'D:\temp_data\tf_preprocess\mf.dev.txt','a',encoding='utf-8') as f:
    for name,label in zip(test_names,test_labels):

        f.write(label +'\t'+name[-1]+'\n')

with open(r'D:\temp_data\tf_preprocess\mf.test.txt','a',encoding='utf-8') as f:
    for name,label in zip(test_names,test_labels):

        f.write(label +'\t'+name[-1]+'\n')
