"""
Step 1 of 4: raw extract. Confirms the Spotify API call and auth work,
prints the raw JSON response. See api_load_version_4.py for the final pipeline.
"""

import datetime
import os

import requests

USER_ID = os.getenv("SPOTIFY_USER_ID")
TOKEN = os.getenv("SPOTIFY_TOKEN")

if __name__ == "__main__":

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}",
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    r = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp),
        headers=headers,
    )

    data = r.json()

    print(data)
