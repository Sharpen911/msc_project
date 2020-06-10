from tqdm import tqdm
import pandas as pd
import numpy
import pickle
import utils
from emoji_extractor.extract import Extractor


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
                if self.detect_emoji(string):
                    tweets_contain_emoji+=1
                running_total.update(self.count_emoji(string, check_first=check_first))

            return running_total,tweets_contain_emoji
        except:
            raise TypeError('This method requires an iterable of strings.')





class Emoji_Analyzer:
    def __init__(self,city = '',user_inf_path = utils.data_path,tweets_path = utils.tweets_save_dir):
        self.city = city
        self.target_dir = tweets_path+city

        df = pd.read_csv(user_inf_path+city+'.csv', index_col='user_id', usecols=['user_id', 'gender', 'ethnicity'])#read the file that store the user information
        self.user_demog = df.to_dict('index')  # a hashmap that maps user_id to their demographic information

        self.collected_tweets = listdir(self.target_dir)

        num_of_users = len(self.collected_tweets)
        self.usage_per_user = pd.DataFrame(numpy.zeros(shape=(num_of_users,num_of_emojis)),columns = possible_emojis)#possible emojis and its number is defined outside

        self.usage_by_male = Counter()
        self.usage_by_female = Counter()
        self.usage_by_asian = Counter()
        self.usage_by_black = Counter()
        self.usage_by_hispanic = Counter()
        self.usage_by_white = Counter()
        self.usage_by_other = Counter()
        self.overall_usage = Counter()

        self.analysis_status = False

    def begin_analysis(self):
        if self.analysis_status:
            print('Analysis already completed')

        extractor = edited_extractor()

        for enum,user_csv in enumerate(tqdm(self.collected_tweets)):

            user_id = int(user_csv[:-11])#get the user id by using the name of a csv file

            user_file = pd.read_csv(self.target_dir+'/'+user_csv)
            user_tweets_list = user_file.text.tolist()

            count,tweets_contain_emoji= extractor.count_all_emoji(user_tweets_list)

            for emoji in count:
                self.usage_per_user.at[enum, emoji] = count[emoji]

            self.usage_per_user.at[enum,'tweets_contain_emoji'] = tweets_contain_emoji
            self.usage_per_user.at[enum,'total_tweets'] = len(user_tweets_list)


            if self.user_demog[user_id]['gender'] == 'male':
                self.usage_per_user.at[enum,'gender'] = 1
            elif self.user_demog[user_id]['gender'] == 'female':
                self.usage_per_user.at[enum,'gender'] = 0

            if self.user_demog[user_id]['ethnicity'] == 'asian':
                self.usage_per_user.at[enum,'ethnicity'] = 1
            elif self.user_demog[user_id]['ethnicity'] == 'black':
                self.usage_per_user.at[enum,'ethnicity'] = 2
            elif self.user_demog[user_id]['ethnicity'] == 'hispanic':
                self.usage_per_user.at[enum,'ethnicity'] = 3
            elif self.user_demog[user_id]['ethnicity'] == 'white':
                self.usage_per_user.at[enum,'ethnicity'] = 4
            elif self.user_demog[user_id]['ethnicity'] == 'other':
                self.usage_per_user.at[enum,'ethnicity'] = 5

            self.overall_usage.update(count)

            if self.user_demog[user_id]['gender'] == 'male':
                self.usage_by_male.update(count)
            elif self.user_demog[user_id]['gender'] == 'female':
                self.usage_by_female.update(count)

            if self.user_demog[user_id]['ethnicity'] == 'asian':
                self.usage_by_asian.update(count)
            elif self.user_demog[user_id]['ethnicity'] == 'black':
                self.usage_by_black.update(count)
            elif self.user_demog[user_id]['ethnicity'] == 'hispanic':
                self.usage_by_hispanic.update(count)
            elif self.user_demog[user_id]['ethnicity'] == 'white':
                self.usage_by_white.update(count)
            elif self.user_demog[user_id]['ethnicity'] == 'other':
                self.usage_by_other.update(count)

        print('Analysis completed')
        self.analysis_status = True

    def save_analysis_results(self,save_dir = 'analysis_results'):
        if self.analysis_status == False:
            print('Please do the analysis before generate results')

        else:
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)

            save_path = save_dir+'/'+'{}_results.pkl'.format(self.city)
            results = {'overall':self.overall_usage,
                       'gender':{'male':self.usage_by_male ,'female':self.usage_by_female},
                       'ethnicity':{'asian':self.usage_by_asian,'black':self.usage_by_black,
                       'hispanic':self.usage_by_hispanic,'white':self.usage_by_white,
                       'other':self.usage_by_other}}


            with open(save_path, 'wb') as file:
                pickle.dump(results, file)

            per_user_path = 'usage_per_user/'+self.city+'_df.pkl'
            self.usage_per_user.to_pickle(per_user_path)


            print('Save the result of {} to {}'.format(self.city,save_path))
            print('Save the usage of the user in {} to {}'.format(self.city, per_user_path))





with open('possible_emoji.pkl', 'rb') as f:
    possible_emojis = pickle.load(f)
    num_of_emojis = len(possible_emojis)
    possible_emojis = sorted(possible_emojis)


cities = ['joh','lon','nyc','ran']

for city in cities:
    analyzer = Emoji_Analyzer(city)
    analyzer.begin_analysis()
    analyzer.save_analysis_results()

# df = a.usage_per_user
# df.loc['Total'] = df.sum()



# df.drop(['total_tweets', 'tweets_contain_emoji','gender','ethnicity'], axis=1,inplace=True)
# test = df.sort_values(by = 'Total',axis=1, ascending=False)#sort the columns by the column sum
#
# print(test.drop([i for i in range(95)], axis=0))
# print(df[df.gender.eq(0)])#filter the column where the gender is female
# print(a.usage_by_female)




# import time
# start_time = time.time()
#
#
# print("--- %s mini-seconds ---" % (time.time() - start_time))


# extract = Extractor()
# for city in utils.cities:
#     df = pd.read_csv(utils.data_path+city+'.csv', index_col='user_id', usecols=['user_id', 'gender', 'ethnicity'])#'data/' + [city name]
#     user_demog = df.to_dict('index')  # hashmap that map user_id to their demographic information
#
#
#
#     users_csv_files = listdir(utils.save_dir+city)
#     for user_csv in users_csv_files:
#
#
#
#         user_file = pd.read_csv(utils.save_dir+city+'/'+user_csv)
#         user_tweets_list = user_file.text.tolist()
#         count = extract.count_all_emoji(user_tweets_list)
#         print((count.most_common()))
#
#         user_id = user_csv[:-11]  # ignore the ending '_tweets.csv' to get the user id


        # with open(city+'_'+'analysis.csv','a+', newline='') as csvfile:
        #     fieldname = ['user_id','ethnicity','gender']
        #     writer = csv.DictWriter(csvfile,fieldnames=fieldname)
        #     writer.writerow({'user_id':user_id,'ethnicity':user_demog[int(user_id)]['ethnicity'],'gender':user_demog[int(user_id)]['gender']})


# context1 = Counter()
#
# dict1 = {'😉': 2, '⭐': 1, '🎖': 1, '😭': 3}
# dict2 = {'😉': 5, '⭐': 3, '🎖': 1}
#
# context1.update(dict1)
# context1.update(dict2)
# print(context1)