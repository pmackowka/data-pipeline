"""
Cloud Function triggered by a GCS object-finalize event: fires a Dataflow
(Apache Beam) job that reads the freshly landed CSV, applies the UDF, and
loads the result into BigQuery.
"""

import os

import google.auth
from googleapiclient.discovery import build

PROJECT_ID = os.environ["GCP_PROJECT_ID"]
REGION = "europe-central2"
TEMPLATE_LOCATION = f"gs://dataflow-templates-{REGION}/latest/GCS_Text_to_BigQuery"
METADATA_BUCKET = "012-ranking-data-metadata"


def trigger_df_job(event, context):
    bucket_name = event["bucket"]
    file_name = event["name"]

    credentials, _ = google.auth.default()
    service = build("dataflow", "v1b3", credentials=credentials)

    template_body = {
        "jobName": "bq-data-flow",
        "parameters": {
            "javascriptTextTransformGcsPath": f"gs://{METADATA_BUCKET}/udf.js",  # UDF
            "JSONPath": f"gs://{METADATA_BUCKET}/bq.json",  # BigQuery schema
            "javascriptTextTransformFunctionName": "transform",  # UDF function name
            "outputTable": f"{PROJECT_ID}.temp.batsmen_rankings",  # BigQuery table
            "inputFilePattern": f"gs://{bucket_name}/{file_name}",  # Uploaded CSV file
            "bigQueryLoadingTemporaryDirectory": f"gs://{METADATA_BUCKET}/temp",
        },
    }

    request = service.projects().locations().templates().launch(
        projectId=PROJECT_ID,
        location=REGION,
        gcsPath=TEMPLATE_LOCATION,
        body=template_body,
    )

    response = request.execute()

    print(f"Dataflow job triggered for file {file_name}: {response}")
