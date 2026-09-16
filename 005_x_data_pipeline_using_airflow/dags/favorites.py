import os

import pandas as pd
import tweepy
from dotenv import load_dotenv

load_dotenv()


def run_favorites():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    authentication_token = os.getenv("AUTHENTICATION_TOKEN")
    authentication_secret = os.getenv("AUTHENTICATION_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(authentication_token, authentication_secret)

    api = tweepy.API(auth)

    try:
        tweets = api.favorites(count=10, tweet_mode='extended')
        print(f"Found {len(tweets)} favorited tweets.")
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
    df.to_csv('favorites_tweets.csv', index=False)
    print("Saved data to favorites_tweets.csv")


if __name__ == "__main__":
    run_favorites()
