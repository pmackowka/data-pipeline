"""
Step 3 of 4: add data-quality checks on top of the version 2 extract.

check_if_valid_data() verifies the frame isn't empty, that 'played_at' is
unique (primary key), that there are no nulls, and warns about rows that
fall outside the expected date window. Not yet wired into the main flow
here -- see api_load_version_4.py, where it gates the load step.
"""

import datetime
import os

import pandas as pd
import requests

USER_ID = os.getenv("SPOTIFY_USER_ID")
TOKEN = os.getenv("SPOTIFY_TOKEN")


def check_if_valid_data(df: pd.DataFrame) -> bool:
    if df.empty:
        print("No songs downloaded. Finishing execution")
        return False

    if not pd.Series(df['played_at']).is_unique:
        raise Exception("Primary Key check is violated")

    if df.isnull().values.any():
        raise Exception("Null values found")

    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).date()

    timestamps = df["timestamp"].tolist()
    for timestamp in timestamps:
        timestamp_date = datetime.datetime.strptime(timestamp, '%Y-%m-%d').date()
        if timestamp_date != yesterday:
            print(f"Warning: A song with timestamp {timestamp} is not from yesterday.")

    return True


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

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps,
    }

    song_df = pd.DataFrame(song_dict, columns=["song_name", "artist_name", "played_at", "timestamp"])

    print(song_df)
