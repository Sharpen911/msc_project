from os import listdir
import pandas as pd
from datetime import datetime as dt

new_path = '/disk/data/share/s1931563/msc_project/src/collected_tweets/'

old_path = '/disk/data/share/s1931563/tweet_data/'

cities = ['joh','lon','nyc','ran']

for city in cities:
    old_tweets = listdir(old_path+city)
    new_tweets = listdir(new_path+city)

    intersec = set.intersection(set(old_tweets), set(new_tweets))

    for file in intersec:
        new = pd.read_csv(new_path + city + '/' + file)
        old = pd.read_csv(old_path + city + '/tweets_' + file)

        #compare the time of last tweets of new data to the first tweets old data
        if dt.strptime(new.created_at.iloc[-1], "%Y-%m-%d %H:%M:%S") >= dt.strptime(old.created_at.iloc[0], "%Y-%m-%d %H:%M:%S"):
            print('User {} need to be updated'.format(new))




# for city in cities:
#     df = pd.read_csv('/disk/data/share/s1931563/msc_project/src/user_data/' + city+'.csv')
#     all_ids = df.user_id.tolist()
#
#     ideal_tweets = [str(id)+'_tweets.csv' for id in all_ids]
#     old_tweets = listdir(old_path+city)
#     new_tweets = listdir(new_path + city)
#
#     to_be_moved = set.intersection(set(ideal_tweets),set(old_tweets)) - set(new_tweets)
#     print('There are {} of user tweets to be moved'.format(len(to_be_moved)))


