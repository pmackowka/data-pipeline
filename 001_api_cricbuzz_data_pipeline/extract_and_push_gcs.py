"""
Fetch T20 batsmen rankings from the Cricbuzz API (RapidAPI) and upload them to GCS as CSV.
Runs both locally and inside Cloud Composer/Airflow (see dag_extract_and_push_gcs.py).
"""

import csv
import os

import requests
from google.cloud import storage

API_URL = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/rankings/batsmen"
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]
BUCKET_NAME = "012-ranking-data"
CSV_FILENAME = "batsmen_rankings.csv"

headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com",
}
params = {
    "formatType": "t20",
}

response = requests.get(API_URL, headers=headers, params=params)

if response.status_code == 200:
    data = response.json().get("rank", [])

    if data:
        field_names = ["rank", "name", "country"]

        with open(CSV_FILENAME, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            for entry in data:
                writer.writerow({field: entry.get(field) for field in field_names})

        print(f"Data fetched successfully and written to '{CSV_FILENAME}'")

        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(CSV_FILENAME)
        blob.upload_from_filename(CSV_FILENAME)

        print(f"File {CSV_FILENAME} uploaded to GCS bucket {BUCKET_NAME} as {CSV_FILENAME}")
    else:
        print("No data available from the API.")
else:
    print("Failed to fetch data:", response.status_code)
