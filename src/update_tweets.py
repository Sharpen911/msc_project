from os import listdir
import pandas as pd
from datetime import datetime as dt
import shutil
new_path ='/disk/data/share/s1931563/msc_project/src/collected_tweets/'

old_path = '/disk/data/share/s1931563/tweet_data/'

cities = ['joh','lon','nyc','ran']

for city in cities:
   old_tweets = listdir(old_path+'tweets_'+city)
   new_tweets = listdir(new_path+city)

   intersec = set.intersection(set(old_tweets), set(new_tweets))
   intersec = sorted(intersec)
   for user_csv in intersec:
       new_csv_path = new_path + city + '/' + user_csv
       old_csv_path = old_path + 'tweets_'+city +'/'+ user_csv


       #try:

           #new = pd.read_csv(new_csv_path,usecols = ['created_at'],lineterminator = '\n')
           new = pd.read_csv(new_csv_path)
           old = pd.read_csv(old_csv_path)

           if dt.strptime(str(new.created_at.iloc[-1]), "%Y-%m-%d %H:%M:%S") >= dt.strptime("2019-01-01 06:23:04", "%Y-%m-%d %H:%M:%S"):
               merged = pd.concat([new,old])
               merged.to_csv(new_csv_path,index=False)

# old = pd.read_csv(old_csv_path,lineterminator = '\n')
# old.to_csv(new_csv_path, mode='a', header=False, index=False)

       # except:
       #     print('skip the user {}'.format(user_csv))



# for city in cities:
#     df = pd.read_csv('/disk/data/share/s1931563/msc_project/src/user_data/' + city+'.csv')
#     all_ids = df.user_id.tolist()
#
#     ideal_tweets = [str(id)+'_tweets.csv' for id in all_ids]
#     old_tweets = listdir(old_path+'tweets_'+city)
#     new_tweets = listdir(new_path + city)
#
#
#
#     to_be_moved = set.intersection(set(ideal_tweets),set(old_tweets)) - set(new_tweets)
#     print(len(to_be_moved))
#     for user_csv in to_be_moved:
#         new_csv_path = new_path + city + '/' + user_csv
#         old_csv_path = old_path + 'tweets_' + city + '/' + user_csv
#         shutil.copyfile(old_csv_path,new_csv_path)



