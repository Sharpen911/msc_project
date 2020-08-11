from tqdm import tqdm
import pandas as pd
import numpy
import pickle
import utils
from emoji_extractor.extract import Extractor

import gensim.models as gs
import nltk.tokenize as tk
import phrase2vec as p2v


import os
from os import listdir
from os.path import isfile, join
from collections import Counter


class edited_extractor(Extractor):

    def count_all_emoji(self, iterable, check_first=True):
        running_total = Counter()
        tweets_contain_emoji = 0
        if type(iterable) == str:
            raise TypeError("This method is not for single strings. Use count_emoji() instead")

        try:
            for string in iterable:
                if isinstance(string, str):
                    if self.detect_emoji(string):
                        tweets_contain_emoji += 1

                    running_total.update(self.count_emoji(string, check_first=check_first))

            return running_total, tweets_contain_emoji
        except:
            raise TypeError('This method requires an iterable of strings.')





class Emoji_Analyzer:
    def __init__(self,city = '',user_inf_path = utils.data_path,tweets_path = utils.tweets_save_dir):
        self.city = city
        self.target_dir = tweets_path+city


        user_information = pd.read_csv(user_inf_path+city+'.csv',index_col='user_id',usecols=['user_id', 'gender', 'ethnicity'])#read the file that store the user information
        self.user_demog = user_information.dropna().to_dict('index')  # a hashmap that maps user_id to their demographic information
        labeled = self.user_demog.keys()
        collected = [int(name[:-11]) for name in listdir(utils.tweets_save_dir + city)]

        self.labeled_users = set.intersection(set(labeled), set(collected))

        num_of_users = len(self.labeled_users)

        self.usage_per_user = pd.DataFrame(numpy.zeros(shape=(num_of_users,num_of_emojis)),columns = possible_emojis)#possible emojis and its number is defined outside

        self.analysis_status = False

    def begin_analysis(self):
        if self.analysis_status:
            print('Analysis already completed')

        extractor = edited_extractor()

        for enum, labeled_user in enumerate(tqdm(self.labeled_users)):

            try:

                user_csv = str(labeled_user)+'_tweets.csv'
                user_file = pd.read_csv(self.target_dir+'/'+user_csv, lineterminator='\n',usecols= ['text'])
                user_tweets_list = user_file.text.tolist()

                count, tweets_contain_emoji= extractor.count_all_emoji(user_tweets_list)

                for emoji in count:
                    self.usage_per_user.at[enum, emoji] = count[emoji]

                self.usage_per_user.at[enum, 'tweets_contain_emoji'] = tweets_contain_emoji
                self.usage_per_user.at[enum, 'total_tweets'] = len(user_tweets_list)

                # self.usage_per_user.at[enum, 'user_id'] = int(labeled_user)



                self.usage_per_user.at[enum,'gender'] = self.user_demog[labeled_user]['gender']



                self.usage_per_user.at[enum,'ethnicity'] = self.user_demog[labeled_user]['ethnicity']



            except Exception as e:
                print(e)





        print('Analysis of {} has been completed'.format(self.city))
        self.analysis_status = True

    def save_analysis_results(self,save_dir = 'analysis_results'):
        if self.analysis_status == False:
            print('Please do the analysis before generate results')

        else:

            per_user_path = 'usage_per_user/'+self.city+'_df.pkl'
            self.usage_per_user.to_pickle(per_user_path)

            print('Save the usage by each user in {} to {}'.format(self.city, per_user_path))





with open('possible_emoji.pkl', 'rb') as f:
    possible_emojis = pickle.load(f)
    num_of_emojis = len(possible_emojis)
    possible_emojis = sorted(possible_emojis)


cities = ['joh', 'lon', 'nyc', 'ran']

for city in cities:
    analyzer = Emoji_Analyzer(city)
    analyzer.begin_analysis()
    analyzer.save_analysis_results()





