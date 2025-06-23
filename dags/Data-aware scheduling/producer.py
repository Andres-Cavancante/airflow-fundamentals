from datetime import datetime, timedelta
import random
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.datasets import Dataset

default_args = {
    "owner": "andres",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}

FILE_PATH = r"text.txt"

def generate_word_num(task_instance):
    task_instance.xcom_push(key="number", value=random.randint(2, 9))

def generate_phrase(task_instance):
    number = task_instance.xcom_pull(task_ids="generate_word_num", key="number")
    print(f"Generating {number} words!")

    phrase = " ".join(["any","thing","counts","to","generate","a","word","in","this","function","infinity","and","beyond"][0: number])
    task_instance.xcom_push(key="phrase", value=phrase)

    print(phrase)

def write_file(task_instance):
    try:
        with open(FILE_PATH, "w") as f:
            f.write(task_instance.xcom_pull(task_ids="generate_phrase", key="phrase"))
        print(f"File {FILE_PATH} successfully written")
    except Exception as e:
        print(f"Error: {e}")

with DAG(
    dag_id="generate_words",
    description="DAG to generate words",
    default_args=default_args,
    start_date=datetime(2025, 6, 20),
    schedule="@daily"
) as dag:
    task1 = PythonOperator(
        task_id="generate_number_of_words",
        python_callable=generate_word_num
    )

    task2 = PythonOperator(
        task_id="generate_phrase",
        python_callable=generate_phrase
    )

    task3 = PythonOperator(
        task_id="write_file",
        python_callable=write_file,
        outlets=[Dataset(FILE_PATH)]
    )

    task1 >> task2 >> task3