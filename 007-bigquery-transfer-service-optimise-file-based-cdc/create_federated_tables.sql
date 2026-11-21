CREATE OR REPLACE EXTERNAL TABLE `your-gcp-project-id.temp.customer_federated_tables`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://data_stream_gcs/007_bigquery_transfer_service_optimise_file_based_cdc/*.parquet']
);
