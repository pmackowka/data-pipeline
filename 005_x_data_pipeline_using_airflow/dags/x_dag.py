from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from search_tweets import run_twitter_etl

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'x_dag',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
)

run_etl = PythonOperator(
    task_id='complete_x_etl',
    python_callable=run_twitter_etl,
    dag=dag,
)

run_etl