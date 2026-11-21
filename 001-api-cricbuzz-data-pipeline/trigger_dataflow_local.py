"""
Local entry point for manually firing the same Dataflow job as trigger_dataflow.py,
without waiting for a real GCS event. Requires GOOGLE_APPLICATION_CREDENTIALS and
GCP_PROJECT_ID to be set in the environment before running.
"""

import os

from googleapiclient.discovery import build

PROJECT_ID = os.environ["GCP_PROJECT_ID"]
REGION = "europe-central2"
TEMPLATE_LOCATION = f"gs://dataflow-templates-{REGION}/latest/GCS_Text_to_BigQuery"
METADATA_BUCKET = "012-ranking-data-metadata"
INPUT_BUCKET = "012-ranking-data"


def trigger_df_job_local():
    service = build("dataflow", "v1b3")

    template_body = {
        "jobName": "bq-data-flow",
        "parameters": {
            "javascriptTextTransformGcsPath": f"gs://{METADATA_BUCKET}/udf.js",  # UDF
            "JSONPath": f"gs://{METADATA_BUCKET}/bq.json",  # BigQuery schema
            "javascriptTextTransformFunctionName": "transform",  # UDF function name
            "outputTable": f"{PROJECT_ID}.temp.batsmen_rankings",  # BigQuery table
            "inputFilePattern": f"gs://{INPUT_BUCKET}/batsmen_rankings.csv",  # Input file
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
    print(f"Dataflow job triggered: {response}")


if __name__ == "__main__":
    trigger_df_job_local()
