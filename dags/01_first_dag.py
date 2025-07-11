from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "andres", #REVIEW - why?
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}

with DAG(
    dag_id="first_dag",
    description="First airflow dag",
    default_args=default_args,
    start_date=datetime(2025, 3, 18, 12),
    schedule_interval="@daily"
) as dag:
    task1 = BashOperator(
        task_id="first_task",
        bash_command="echo hello,world"
    )