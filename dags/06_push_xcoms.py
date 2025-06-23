from datetime import timedelta, datetime
import random
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "andres",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}

def greet(task_instance):
    name = task_instance.xcom_pull(task_ids="get_name_and_age", key="name")
    age = task_instance.xcom_pull(task_ids="get_name_and_age", key="age")
    print(f"Hello, World! My name is {name} and I am {age} years old!")

def get_name_and_age(task_instance):
    names = ["Carlos", "Louis", "Serge"]
    
    task_instance.xcom_push(key="name", value=random.choice(names))
    task_instance.xcom_push(key="age", value=random.randint(15, 60))

with DAG(
    dag_id="python_dag_push_xcoms",
    default_args=default_args,
    description="Pushing xcoms",
    start_date=datetime(2025, 3, 18, 12),
    schedule_interval="@daily"
) as dag:
    greet_task = PythonOperator(
        task_id="greet",
        python_callable=greet
    ),

    get_name_and_age_task = PythonOperator(
        task_id="get_name_and_age",
        python_callable=get_name_and_age
    )

    get_name_and_age_task >> greet_task
