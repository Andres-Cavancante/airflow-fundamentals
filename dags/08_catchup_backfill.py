from datetime import timedelta, datetime
from airflow.decorators import dag, task

default_args = {
    "owner": "andres",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}

@dag(
    dag_id="catchup_and_backfill",
    default_args=default_args,
    description="Using the catchup and backfill",
    start_date=datetime(2025, 3, 18, 19),
    schedule_interval="@daily",
    catchup=False # This will cause the DAG to not run retroatively
)
def python_dag():

    @task()
    def greet():
        print(f"Hello, World")

    greet()

python_dag()

# backfill can be executed through CLI as follows:
# airflow dags backfill \
    # --start-date START_DATE \
    # --end-date END_DATE \
    # dag_id