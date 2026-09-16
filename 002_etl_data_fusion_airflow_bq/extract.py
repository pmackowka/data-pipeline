"""
Generate a synthetic employee dataset with Faker and upload it to GCS,
where Cloud Data Fusion picks it up for transformation into BigQuery.
"""

import csv
import random
import string

from faker import Faker
from google.cloud import storage

NUM_EMPLOYEES = 100
FIELDNAMES = ["first_name", "last_name", "job_title", "department", "email", "address", "phone_number", "salary", "employee_id"]

fake = Faker()
id_characters = string.ascii_uppercase + string.digits

with open("employee_data.csv", mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=FIELDNAMES, quotechar='"', quoting=csv.QUOTE_ALL)
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
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name} in {bucket_name}.")


bucket_name = "data_stream_gcs"
source_file_name = "employee_data.csv"
destination_blob_name = "002_etl_data_fusion_airflow_bq/employee_data.csv"

upload_to_gcs(bucket_name, source_file_name, destination_blob_name)
