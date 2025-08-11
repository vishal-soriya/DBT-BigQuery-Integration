"""
DBT Multi-Client Transformation DAG

This DAG runs DBT transformations for multiple clients in sequence:
1. Client A: seed -> run -> test
2. Client B: seed -> run -> test

Author: Auto-generated
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

# Default arguments for all tasks
default_args = {
    'owner': 'dbt-admin',
    'depends_on_past': False,
    'start_date': datetime(2025, 8, 11),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    'dbt_multi_client_transformations',
    default_args=default_args,
    description='Run DBT transformations for multiple clients',
    schedule_interval='0 2 * * *',  # Run daily at 2 AM
    catchup=False,
    tags=['dbt', 'multi-client', 'transformations'],
)

# Start task
start = DummyOperator(
    task_id='start',
    dag=dag,
)

# Client A Tasks
client_a_seed = BashOperator(
    task_id='client_a_seed',
    bash_command='cd /opt/airflow/dbt_project && ./run_dbt_client.sh client_a dev seed',
    dag=dag,
)

client_a_run = BashOperator(
    task_id='client_a_run',
    bash_command='cd /opt/airflow/dbt_project && ./run_dbt_client.sh client_a dev run',
    dag=dag,
)

client_a_test = BashOperator(
    task_id='client_a_test',
    bash_command='cd /opt/airflow/dbt_project && ./run_dbt_client.sh client_a dev test',
    dag=dag,
)

# Client B Tasks
client_b_seed = BashOperator(
    task_id='client_b_seed',
    bash_command='cd /opt/airflow/dbt_project && ./run_dbt_client.sh client_b dev seed',
    dag=dag,
)

client_b_run = BashOperator(
    task_id='client_b_run',
    bash_command='cd /opt/airflow/dbt_project && ./run_dbt_client.sh client_b dev run',
    dag=dag,
)

client_b_test = BashOperator(
    task_id='client_b_test',
    bash_command='cd /opt/airflow/dbt_project && ./run_dbt_client.sh client_b dev test',
    dag=dag,
)

# End task
end = DummyOperator(
    task_id='end',
    dag=dag,
)

# Define task dependencies
# Client A pipeline
start >> client_a_seed >> client_a_run >> client_a_test

# Client B pipeline (runs after Client A completes)
client_a_test >> client_b_seed >> client_b_run >> client_b_test >> end
