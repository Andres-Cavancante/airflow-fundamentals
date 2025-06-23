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
    name = task_instance.xcom_pull(task_ids="get_name") #This will get the value returned by the function
    age = task_instance.xcom_pull(task_ids="get_age")
    print(f"Hello, World! My name is {name} and I am {age} years old!")

def get_name():
    names = ["Carlos", "Louis", "Serge"]
    return random.choice(names)

def get_age():
    return random.randint(15, 60)

with DAG(
    dag_id="python_dag_with_xcoms",
    default_args=default_args,
    description="Using xcoms",
    start_date=datetime(2025, 3, 18, 12),
    schedule_interval="@daily"

) as dag:
    greet_task = PythonOperator(
        task_id="greet",
        python_callable=greet
    ),

    get_age_task = PythonOperator(
        task_id="get_age",
        python_callable=get_age
    )

    get_name_task = PythonOperator(
        task_id="get_name",
        python_callable=get_name
    )

    # get_name_task #This execution will log: "Returned value was: {name}"

    get_age_task >> greet_task
    get_name_task >> greet_task
