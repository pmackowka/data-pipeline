import os

import pandas as pd
import tweepy
from dotenv import load_dotenv

load_dotenv()

SEARCH_QUERY = os.getenv("SEARCH_QUERY", "from:twitterdev")


def run_twitter_etl():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    authentication_token = os.getenv("AUTHENTICATION_TOKEN")
    authentication_secret = os.getenv("AUTHENTICATION_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(authentication_token, authentication_secret)

    api = tweepy.API(auth)

    try:
        tweets = api.search_tweets(q=SEARCH_QUERY, count=200, tweet_mode='extended')
        print(f"Found {len(tweets)} tweets.")
    except Exception as e:
        print(f"Failed to fetch tweets: {e}")
        return

    refined_tweets = []
    for tweet in tweets:
        refined_tweets.append({
            "user": tweet.user.screen_name,
            "text": tweet._json["full_text"],
            "favorite_count": tweet.favorite_count,
            "retweet_count": tweet.retweet_count,
            "created_at": tweet.created_at,
        })

    df = pd.DataFrame(refined_tweets)

    if df.empty:
        print("No data to write to CSV.")
    else:
        df.to_csv('refined_tweets.csv', index=False)
        print("Saved data to refined_tweets.csv")


if __name__ == "__main__":
    run_twitter_etl()
