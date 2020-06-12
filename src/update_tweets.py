from os import listdir
import pandas as pd
from datetime import datetime as dt
import csv
new_path ='/disk/data/share/s1931563/msc_project/src/collected_tweets/'

old_path = '/disk/data/share/s1931563/tweet_data/'

cities = ['joh']
 
for city in cities:
    old_tweets = listdir(old_path+'tweets_'+city)
    new_tweets = listdir(new_path+city)

    intersec = set.intersection(set(old_tweets), set(new_tweets))
   
    for user_csv in intersec:
        new_csv_path = new_path + city + '/' + user_csv
        old_csv_path = old_path + 'tweets_'+city +'/'+ user_csv
        

            
        with open(new_csv_path, "r", encoding="utf-8") as f:
            new = pd.read_csv(new_csv_path,usecols = ['created_at'],lineterminator = '\n')
        #old = pd.read_csv(old_csv_path,usecols = ['created_at'])
        #compare the time of last tweets of new data to the first tweets old data
        
        if dt.strptime(str(new.iloc[-1].values[0]), "%Y-%m-%d %H:%M:%S") >= dt.strptime("2019-01-01 06:23:04", "%Y-%m-%d %H:%M:%S"):
            print('update {}'.format(user_csv))


#
#for city in cities:
#    df = pd.read_csv('/disk/data/share/s1931563/msc_project/src/user_data/' + city+'.csv')
#    all_ids = df.user_id.tolist()
#
#    ideal_tweets = [str(id)+'_tweets.csv' for id in all_ids]
#    old_tweets = listdir(old_path+'tweets_'+city)
#    new_tweets = listdir(new_path + city)
#
#    to_be_moved = set.intersection(set(ideal_tweets),set(old_tweets)) - set(new_tweets)
#    print('There are {} of user tweets to be moved'.format(len(to_be_moved)))


