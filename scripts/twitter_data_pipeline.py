from os import path
import sys
import json

current_path = path.dirname(path.abspath(__file__))
root_path = path.dirname(current_path)
sys.path.append(root_path)
from data_methods import twitter_data_methods as tm

# streaming config
with open('./tokens/twitter_token.json','r') as f_tk:
    tokens = json.load(f_tk)


try:
    keywords_choice = int(sys.argv[1])
except:
    pass

# crypto currency keywords
keywords_choice = ''
if keywords_choice == 'tech':
    track_path = path.join(root_path, 'resources/tech_keywords.txt')
    database_path = path.join(root_path, 'resources/tech_tweets.db')
    print("Starting collecting tech tweets")
# default choice is crypto
if keywords_choice == 'nasdaq':
    track_path = path.join(root_path, 'resources/nasdaq_keywords.txt')
    database_path = path.join(root_path, 'resources/nasdaq_tweets.db')
    print("Starting collecting nasdaq tweets")
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
