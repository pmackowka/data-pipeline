import functions_framework
from google.cloud import bigquery
from google.cloud.bigquery import LoadJobConfig

DATASET = "temp"
TABLE = "orders_ecommerce"
SOURCE_BUCKET = "data_stream_gcs"


@functions_framework.cloud_event
def hello_gcs(cloud_event):
    """Cloud Function triggered by a GCS object-finalize event: loads the new CSV into BigQuery."""
    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]
    filename = data["name"]

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {data['bucket']}")
    print(f"File: {filename}")
    print(f"Metageneration: {data['metageneration']}")
    print(f"Created: {data['timeCreated']}")
    print(f"Updated: {data['updated']}")

    load_bq(filename)


def load_bq(filename):
    client = bigquery.Client()
    table_ref = client.dataset(DATASET).table(TABLE)

    job_config = LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1
    job_config.autodetect = True

    uri = f"gs://{SOURCE_BUCKET}/{filename}"
    load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config)
    load_job.result()  # blocks until the load job finishes

    print(f"{load_job.output_rows} rows loaded into {TABLE}.")
