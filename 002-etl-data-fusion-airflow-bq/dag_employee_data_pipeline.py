from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.providers.google.cloud.operators.datafusion import CloudDataFusionStartPipelineOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'depends_on_past': False,
    'email': ['you@example.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('dag_employee_data_pipeline',
          default_args=default_args,
          description='Runs an external Python script',
          schedule_interval='@daily',
          catchup=False)

with dag:
    extract_data = BashOperator(
        task_id='extract_data',
        bash_command='python /home/airflow/gcs/dags/scripts/extract.py',
    )

    datafusion_pipeline = CloudDataFusionStartPipelineOperator(
        location="europe-north1",  # Data Fusion region
        pipeline_name="employee_data",
        instance_name="datapipeline",  # Data Fusion instance name
        task_id="datafusion_pipeline",
    )

    extract_data >> datafusion_pipeline