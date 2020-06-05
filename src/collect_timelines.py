import tweepy
from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler

import time
import utils
import pandas as pd

import os
from os import listdir
from os.path import isfile, join


# # # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth,wait_on_rate_limit=True,wait_on_rate_limit_notify = True)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

# # # # TWITTER AUTHENTICATER # # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(utils.CONSUMER_KEY, utils.CONSUMER_SECRET)
        auth.set_access_token(utils.ACCESS_TOKEN, utils.ACCESS_TOKEN_SECRET)
        return auth



def save_collected_tweets(save_dir,user_id,tweets):
    dict = {}

    dict['user_id'] = [tweet.user.id for tweet in tweets]
    dict['user_name'] = [tweet.user.name for tweet in tweets]
    dict['user_screen_name'] = [tweet.user.screen_name for tweet in tweets]
    dict['user_statuses_count'] = [tweet.user.statuses_count for tweet in tweets]
    dict['tweet_id'] = [tweet.id for tweet in tweets]
    dict['hashtags'] = [tweet.entities['hashtags'] for tweet in tweets]
    dict['is_quote_status'] = [tweet.is_quote_status for tweet in tweets]
    dict['text'] = [tweet.text for tweet in tweets]
    dict['created_at'] = [tweet.created_at for tweet in tweets]
    dict['source'] = [tweet.source for tweet in tweets]
    dict['in_reply_to_screen_name'] = [tweet.in_reply_to_screen_name for tweet in tweets]

    df = pd.DataFrame(dict)

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    save_path = save_dir + '/' + str(user_id) + '_tweets.csv'

    df.to_csv(save_path, index=False)

def get_all_tweets(user_id,api):
    alltweets = []


    new_tweets = api.user_timeline(id = user_id, count=200)
    if len(new_tweets) == 0:
        return alltweets

    alltweets.extend(new_tweets)

    oldest = alltweets[-1].id - 1

    while len(new_tweets) > 0:

        new_tweets = api.user_timeline(id = user_id, count=200, max_id=oldest)

        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1



    return alltweets


 
if __name__ == '__main__':
    if not os.path.exists('collected_tweets'):
        os.mkdir('collected_tweets')

    twitter_client = TwitterClient()
    api = twitter_client.get_twitter_client_api()

    profiles_path = utils.data_path
    all_profiles = [f for f in listdir(profiles_path) if isfile(join(profiles_path, f))]

    for profiles in all_profiles:
        df = pd.read_csv(profiles_path+profiles)
        user_ids = df.user_id.tolist()
        if profiles == 'joh.csv' :
            collected_files = [int(f[:-11]) for f in listdir('collected_tweets/joh') if isfile(join('collected_tweets/joh', f))]
            intersection_set = set.difference(set(user_ids), set(collected_files))
            user_ids = list(intersection_set)

        for user_id in user_ids:
            try:

                all_tweets = get_all_tweets(user_id, api)
                save_collected_tweets(utils.save_dir + profiles[:-4], user_id,all_tweets)  # use indices to create the folder by location

            except tweepy.TweepError as ex:
                if ex.reason == "Not authorized.":
                    print('The Tweets of user {} are protected,skipping...'.format(user_id))


    # status = api.rate_limit_status()
    # print(status['resources']['statuses']['/statuses/user_timeline'])
