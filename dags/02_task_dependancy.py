from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "andres",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}

with DAG(
    dag_id="task_dependancy_3",
    description="First airflow dag",
    default_args=default_args,
    start_date=datetime(2025, 3, 18, 12),
    schedule_interval="@daily"
) as dag:
    task1 = BashOperator(
        task_id="first_task",
        bash_command="echo hello,world"
    )

    task2 = BashOperator(
        task_id="second_task",
        bash_command="echo this is the second task, running after the first task!"
    )

    task3 = BashOperator(
        task_id="third_task",
        bash_command="echo this is the third task, running after the first task and simultaneously to the second!"
    )

    # first dependency method (task_dependancy):
    # task1.set_downstream(task2) #task1 is upstream for task2
    # task1.set_downstream(task3) #task1 is upstream for task3
    
    # second dependency method (task_dependancy_2):
    # task1 >> task2
    # task1 >> task3

    # simples dependency method, using lists of tasks(task_dependancy_3):
    task1 >> [task2, task3]