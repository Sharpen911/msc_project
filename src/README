## The function of different folders:

collected_tweets: the directory to store collected tweets.

pre-trained: the directory that stores pre-trained embeddings

user_data: the dataset that stores labeled users and their profile information. This enable us to collect them timelines.

(under "jupyter")usage_per_user: the directory that will store pickled file, which is in the form of pandas dataframe.It contains
the emoji usage for all the users that are labeled with both gender and ethnicity.

(under "jupyter")features: stores the features related to embedding methods.

## The function for the codes:

utils.py: save some path, and the account tokens provided by Twitter API.

collect_timelines.py: collecte all the user's tweets and save them.

update_tweets.py: add older tweets for more activated user(Twitter API only return approximately 3200 of users tweets)
notice the older tweets are stored on the server provided by the University of Edinburgh.

tweets_analyzer.py: count emoji frequency for each user, and save it.

phrase2vec.py: this file is provided by the authors of the Emoji2vec. It converts a tweet into a vector,
by using pre-trained embedding models. I cite this in the dissertation.

prepare_features.py: use phrase2vec.py to prepare the features that is related to embedding methods.

## The ipython(jupyter notebook) files under the folder of "jupyter":

analysis: the script for general analysis of emojis usage.

MI_gender,MI_ethnicity,Chi2_gender,Chi2_ethnicity: find most distinctive emojis used by gender/ethnicity,
by using mutual information/Chi-square test.

prediction-BOE: predict gender and ethnicity by using bag of emojis feature(BOE).

confusion matrix: make the confusion matrix.

cross_validate: use cross validation to find hyper-parameters for different models.

The .ipynb file starting with 'embedding': predict gender and ethnicity by using features based on some embedding methods.

