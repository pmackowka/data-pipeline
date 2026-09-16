"""
Local variant of extract.py: generates a small sample and authenticates with an
explicit service account key instead of relying on the runtime's default credentials.
Requires GOOGLE_APPLICATION_CREDENTIALS to point at a local service account key file.
"""

import csv
import os
import random
import string

from faker import Faker
from google.cloud import storage
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

NUM_EMPLOYEES = 10
FIELDNAMES = ["first_name", "last_name", "job_title", "department", "email", "address", "phone_number", "salary", "employee_id"]

fake = Faker()
id_characters = string.ascii_uppercase + string.digits

with open("employee_data_local.csv", mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
    writer.writeheader()

    for _ in range(NUM_EMPLOYEES):
        writer.writerow({
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "job_title": fake.job(),
            "department": fake.job(),
            "email": fake.email(),
            "address": fake.city(),
            "phone_number": fake.phone_number(),
            "salary": fake.random_number(digits=5),
            "employee_id": "".join(random.choice(id_characters) for _ in range(10)),
        })


def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name} in {bucket_name}.")


bucket_name = "data_stream_gcs"
source_file_name = "employee_data_local.csv"
destination_blob_name = "002_etl_data_fusion_airflow_bq/employee_data_local.csv"

upload_to_gcs(bucket_name, source_file_name, destination_blob_name)
