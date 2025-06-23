from datetime import timedelta, datetime
from airflow.decorators import dag, task

default_args = {
    "owner": "andres",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}

# With taskflow api, the decorators @dag() and @task() are available
@dag(
    dag_id="python_dag_taskflow",
    default_args=default_args,
    description="Using taskflow",
    start_date=datetime(2025, 3, 18, 12),
    schedule_interval="@daily"
)
def python_dag():

    @task()
    def get_age():
        return 19
    
    @task(multiple_outputs=True) # This optional parameter allows to return a dictionary. Not necessary for single value
    def get_name():
        return {
            "first": "Carlos",
            "last": "Black"
        }
    
    @task()
    def greet(first_name, last_name, age):
        print(f"Hello, World! My name is {first_name} {last_name} and I am {age} years old!")

    name = get_name()

    greet(name["first"], name["last"], get_age()) # This is an xcom

python_dag()