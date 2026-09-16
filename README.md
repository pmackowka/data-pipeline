# Data Pipeline

A collection of standalone data pipelines built while learning the modern data stack — GCP, Airflow, dbt, and the API/event-driven patterns that connect them. Each project is self-contained: its own README, its own dependencies, runnable on its own.

This isn't one framework wearing seven hats — it's seven different answers to "how do I get data from A to B," picked to cover the patterns that come up most in practice: event-driven triggers, orchestrated ETL, managed no-code transforms, incremental CDC, and a full orchestration + transformation + data-quality stack.

## Projects

| # | Project | Pattern | Stack |
|---|---|---|---|
| 001 | [Cricbuzz Rankings → BigQuery](001_api_cricbuzz_data_pipeline) | REST API → GCS, event-triggered Dataflow load | Airflow/Composer, Cloud Functions, Dataflow, BigQuery |
| 002 | [Employee Data → Data Fusion → BigQuery](002_etl_data_fusion_airflow_bq) | Airflow-orchestrated ETL into a managed no-code transform | Airflow, Cloud Data Fusion, BigQuery |
| 003 | [Browser Upload → GCS → BigQuery](003_loading_data_from_www_page_to_bq) | Manual upload for non-technical users, event-triggered load | Flask, Cloud Functions, BigQuery |
| 004 | [Retail Analytics: Airflow + dbt + Soda](004_airflow_dbt_retail_project) | Full orchestration + transformation + data-quality gate | Airflow (Cosmos), dbt, Soda, BigQuery |
| 005 | [X (Twitter) Data Pipeline](005_x_data_pipeline_using_airflow) | Scheduled API extract via self-hosted Airflow | tweepy, Airflow, Docker Compose |
| 006 | [Spotify Listening History](006_spotify_data_pipeline) | Incremental ELT, built up in four iterations | Spotify API, pandas, SQLite |
| 007 | [File-Based CDC via BigQuery External Tables](007_bigquery_transfer_service_optimise_file_based_cdc) | Query GCS files immediately, before a scheduled load | PyArrow, BigQuery external tables |

Project 004 is the most complete: an Airflow DAG builds a retail star schema with dbt and gates every stage — load, transform, report — on Soda data-quality checks, so a broken model fails the pipeline instead of reaching a dashboard quietly.

## Running a project

Each folder has its own `README.md` and `requirements.txt`. General pattern:

```bash
cd 004_airflow_dbt_retail_project
pip install -r requirements.txt
# see the project's own README for the specific run command and required env vars
```

None of the projects ship credentials. Where a script needs one (a GCP service account, an API key, OAuth tokens), it reads it from an environment variable — set it before running, per the project's README.

## Author

Piotr Maćkówka — Senior Data Analyst / Analytics Architect, e-commerce, currently building out the AI/agentic side of the data engineering stack (Claude Code, MCP, LLM-assisted pipelines).

## License

[MIT](LICENSE)
