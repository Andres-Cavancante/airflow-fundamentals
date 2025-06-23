from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.datasets import Dataset

default_args = {
    "owner": "andres",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}

text_file = Dataset(r"text.txt")

def read_file(task_instance):
    try:
        with open(text_file.uri, "r") as f:
            text = f.read()
            print(text)
            task_instance.xcom_push(key="file_text", value=text)
    except Exception as e:
        print(f"Error: {e}")

with DAG (
    dag_id="count_words",
    default_args=default_args,
    description="DAG to count words",
    start_date=datetime(2025, 6, 20),
    schedule=[text_file]
) as dag:
    tas1 = PythonOperator(
        task_id="read_file",
        python_callable=read_file
    )