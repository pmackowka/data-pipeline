import os
import uuid

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from faker import Faker
from google.cloud import storage
from google.oauth2 import service_account

# Initialize Faker to generate synthetic sample data
fake = Faker()

# Number of rows per file
NUM_ROWS = 10000
# Number of files to generate, simulating incremental CDC batches
NUM_FILES = 10

bucket_name = os.getenv('BUCKET_NAME')  # e.g. "my-bucket/customer_data"

credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
credentials = service_account.Credentials.from_service_account_file(credentials_path)
storage_client = storage.Client(credentials=credentials)

bucket_root, folder_path = bucket_name.split('/')

for i in range(NUM_FILES):
    data = []
    for _ in range(NUM_ROWS):
        data.append({
            "id": str(uuid.uuid4()),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "phone_number": fake.phone_number(),
            "address": fake.address(),
            "city": fake.city(),
            "state": fake.state(),
            "zip_code": fake.zipcode(),
            "country": fake.country(),
            "birthdate": fake.date_of_birth(minimum_age=18, maximum_age=80),
            "gender": fake.random_element(elements=("Male", "Female", "Other")),
        })

    df = pd.DataFrame(data)
    table = pa.Table.from_pandas(df)

    file_path = f"{folder_path}/customer_data_{i}.parquet"

    blob = storage_client.bucket(bucket_root).blob(file_path)
    with blob.open("wb") as f:
        pq.write_table(table, f)

    print(f"Wrote {NUM_ROWS} customer rows to gs://{bucket_root}/{file_path}")
