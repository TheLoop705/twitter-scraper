import os

import tweepy
from dotenv import load_dotenv

load_dotenv()

bearer_token = os.environ["BEARER_TOKEN"]
target_user = os.environ["TARGET_USER"]
if bearer_token is None or target_user is None:
    raise TypeError("Please provide authentication token and target user")

# https://docs.tweepy.org/en/stable/authentication.html

client = tweepy.Client(bearer_token)
# Possible endpoints <- https://docs.tweepy.org/en/stable/client.html

user_id = client.get_user(username=target_user, user_fields=["username", "id"]).data.id

# tweet fields 'id,text,entities,created_at,geo,in_reply_to_user_id
# ,lang,public_metrics,source'
tweet_fields = ["id", "text", "created_at"]
res = client.get_users_tweets(id=user_id, tweet_fields=tweet_fields, max_results=5)

tweets = {}  # id: text
for tweet in res.data:
    tweets[tweet.id] = tweet.text

for key, value in tweets.items():
    print("Tweet ID: %d, Text: %s \n" % (key, value))

with open("tweets.csv", "w") as f:
    f.write("Tweet ID,Text")
    f.write("\n")
    for key, value in tweets.items():
        text = value.encode("ascii", "ignore").decode("ascii")
        text = text.replace(",", " ").replace("\n", " ")
        f.write("%d,%s" % (key, text))
        f.write("\n")
