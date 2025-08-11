"""
DBT Production Deployment DAG

This DAG handles production deployments:
1. Run specific models for production
2. Includes data quality checks
3. Notification on completion

Author: Auto-generated
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

def send_success_notification(**context):
    """Send notification when DAG succeeds"""
    print("🎉 DBT Production deployment completed successfully!")
    print(f"Execution Date: {context['execution_date']}")
    print(f"DAG Run ID: {context['run_id']}")
    # You can add email/Slack notifications here

def send_failure_notification(**context):
    """Send notification when DAG fails"""
    print("❌ DBT Production deployment failed!")
    print(f"Task ID: {context['task_instance'].task_id}")
    print(f"Exception: {context['exception']}")
    # You can add email/Slack notifications here

# Default arguments for all tasks
default_args = {
    'owner': 'dbt-admin',
    'depends_on_past': False,
    'start_date': datetime(2025, 8, 11),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=10),
    'on_failure_callback': send_failure_notification,
    'on_success_callback': send_success_notification,
}

# Create the DAG
dag = DAG(
    'dbt_production_deployment',
    default_args=default_args,
    description='DBT Production deployment with quality checks',
    schedule_interval=None,  # Manual trigger only
    catchup=False,
    tags=['dbt', 'production', 'deployment'],
)

# Pre-deployment checks
start = DummyOperator(
    task_id='start_deployment',
    dag=dag,
)

# Client A Production Tasks
client_a_prod_run = BashOperator(
    task_id='client_a_prod_run',
    bash_command='cd /opt/airflow/dbt_project && ./run_dbt_client.sh client_a prod run',
    dag=dag,
)

client_a_prod_test = BashOperator(
    task_id='client_a_prod_test',
    bash_command='cd /opt/airflow/dbt_project && ./run_dbt_client.sh client_a prod test',
    dag=dag,
)

# Client B Production Tasks
client_b_prod_run = BashOperator(
    task_id='client_b_prod_run',
    bash_command='cd /opt/airflow/dbt_project && ./run_dbt_client.sh client_b prod run',
    dag=dag,
)

client_b_prod_test = BashOperator(
    task_id='client_b_prod_test',
    bash_command='cd /opt/airflow/dbt_project && ./run_dbt_client.sh client_b prod test',
    dag=dag,
)

# Generate documentation
generate_docs = BashOperator(
    task_id='generate_docs',
    bash_command='cd /opt/airflow/dbt_project && ./run_dbt_client.sh client_a prod docs',
    dag=dag,
)

# Success notification
success_notification = PythonOperator(
    task_id='success_notification',
    python_callable=send_success_notification,
    dag=dag,
)

# Define task dependencies
start >> [client_a_prod_run, client_b_prod_run]

# Client pipelines
client_a_prod_run >> client_a_prod_test
client_b_prod_run >> client_b_prod_test

# Final steps
[client_a_prod_test, client_b_prod_test] >> generate_docs >> success_notification
