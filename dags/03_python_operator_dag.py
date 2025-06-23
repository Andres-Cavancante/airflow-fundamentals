from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "andres",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}

def greet():
    print("Hello, World!")

with DAG(
    dag_id="python_operator_dag",
    default_args=default_args,
    description="First airflow dag with python operator",
    start_date=datetime(2025, 3, 18, 12),
    schedule_interval="@daily"

) as dag:
    task1 = PythonOperator(
        task_id="greet",
        python_callable=greet
    )