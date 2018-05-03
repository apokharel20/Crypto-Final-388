from os import path
import sys

current_path = path.dirname(path.abspath(__file__))
root_path = path.dirname(current_path)
sys.path.append(root_path)
from data_methods import twitter_data_methods as tm

# streaming config
tokens = {
    'access_token': "991762847431577600-oEE9jJJGop7ryuxlFrV0hGh23mTeVsr",
    'access_token_secret': "UVQF3XVLOTQ6ts9ExjLvSkqKoXKP2t8ymsNXib7pPk7t7",
    'consumer_key': "hfVB97jMLkaxy3JZDyLNrq44R",
    'consumer_secret': "WStsierspsfDXCLwzeXEnUyks6QDtPpS0Z8jxp7FMDXlDNz0dV"
}

keywords_choice = 0
try:
    keywords_choice = int(sys.argv[1])
except:
    pass

# crypto currency keywords

if keywords_choice == 1:
    track_path = path.join(root_path, 'resources/tech_keywords.txt')
    database_path = path.join(root_path, 'resources/tech_tweets.db')
    print("Starting collecting tech tweets")

else:
    track_path = path.join(root_path, 'resources/crypto_keywords.txt')
    database_path = path.join(root_path, 'resources/crypto_tweets.db')
    print("Starting collecting crypto tweets")



with open(track_path, 'r') as f:
    stock_symbol = f.read()
    track = stock_symbol.split(",")

# filter config
tweet_filter = tm.key_word_filter(track)

# format config
tweet_formator = tm.twitter_format()

# database config

tweet_database = tm.twitter_database(database_path)

# start the pipeline
twitter_data_pipeline = tm.twitter_streaming(tokens, track, tweet_filter, tweet_formator, tweet_database)
twitter_data_pipeline.run()
