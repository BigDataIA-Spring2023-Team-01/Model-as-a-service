from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from datetime import datetime




def say_hello():
    print("Hello world")
    return "Hello world"

def say_bye():
    print("Bye")
    return "Bye"

# Define the DAG
dag = DAG('my_dag', description='Example DAG for saying hello',
          schedule_interval=None, start_date=datetime(2023, 3, 24))

# Define the tasks
task1 = PythonOperator(task_id='say_hello', python_callable=say_hello, dag=dag)
task2 = PythonOperator(task_id='say_bye', python_callable=say_bye, dag=dag)

# Define the task dependencies
task1 >> task2
