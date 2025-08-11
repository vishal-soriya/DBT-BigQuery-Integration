"""
Advanced DBT Multi-Client DAG using Custom Operators

This DAG uses custom DBT operators for better monitoring and error handling.
Includes data quality checks and notifications.

Author: Auto-generated
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

# Import custom DBT operators
import sys
import os
sys.path.append('/opt/airflow/plugins')
from dbt_operators import DBTRunOperator, DBTTestOperator, DBTSeedOperator

def check_data_quality(**context):
    """Check data quality from previous tasks"""
    
    # Get results from previous tasks
    client_a_results = context['task_instance'].xcom_pull(task_ids='client_a_test')
    client_b_results = context['task_instance'].xcom_pull(task_ids='client_b_test')
    
    total_errors = 0
    
    if client_a_results and client_a_results.get('error', 0) > 0:
        total_errors += client_a_results['error']
        
    if client_b_results and client_b_results.get('error', 0) > 0:
        total_errors += client_b_results['error']
    
    print(f"📊 Data Quality Summary:")
    print(f"   Client A Results: {client_a_results}")
    print(f"   Client B Results: {client_b_results}")
    print(f"   Total Errors: {total_errors}")
    
    if total_errors > 0:
        raise ValueError(f"Data quality check failed! {total_errors} errors found.")
    
    print("✅ All data quality checks passed!")
    return {"status": "passed", "total_errors": total_errors}

def send_completion_report(**context):
    """Send completion report with metrics"""
    
    execution_date = context['execution_date']
    dag_run = context['dag_run']
    
    print(f"📋 DBT Multi-Client Execution Report")
    print(f"   Execution Date: {execution_date}")
    print(f"   DAG Run ID: {dag_run.run_id}")
    print(f"   Status: Completed Successfully")
    print(f"   Duration: {datetime.now() - execution_date}")
    
    # Here you could send email, Slack notification, etc.
    return {"report_sent": True}

# Default arguments
default_args = {
    'owner': 'dbt-admin',
    'depends_on_past': False,
    'start_date': datetime(2025, 8, 11),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    'dbt_advanced_multi_client',
    default_args=default_args,
    description='Advanced DBT multi-client workflow with custom operators',
    schedule_interval='0 3 * * *',  # Run daily at 3 AM
    catchup=False,
    tags=['dbt', 'advanced', 'multi-client', 'monitoring'],
)

# Start
start = DummyOperator(
    task_id='start',
    dag=dag,
)

# Client A Pipeline using custom operators
client_a_seed = DBTSeedOperator(
    task_id='client_a_seed',
    client='client_a',
    environment='dev',
    dag=dag,
)

client_a_run = DBTRunOperator(
    task_id='client_a_run',
    client='client_a',
    environment='dev',
    dag=dag,
)

client_a_test = DBTTestOperator(
    task_id='client_a_test',
    client='client_a',
    environment='dev',
    dag=dag,
)

# Client B Pipeline using custom operators
client_b_seed = DBTSeedOperator(
    task_id='client_b_seed',
    client='client_b',
    environment='dev',
    dag=dag,
)

client_b_run = DBTRunOperator(
    task_id='client_b_run',
    client='client_b',
    environment='dev',
    dag=dag,
)

client_b_test = DBTTestOperator(
    task_id='client_b_test',
    client='client_b',
    environment='dev',
    dag=dag,
)

# Data quality check
quality_check = PythonOperator(
    task_id='data_quality_check',
    python_callable=check_data_quality,
    dag=dag,
)

# Completion report
completion_report = PythonOperator(
    task_id='send_completion_report',
    python_callable=send_completion_report,
    dag=dag,
)

# End
end = DummyOperator(
    task_id='end',
    dag=dag,
)

# Define dependencies - Parallel execution with quality gates
start >> [client_a_seed, client_b_seed]

# Client A pipeline
client_a_seed >> client_a_run >> client_a_test

# Client B pipeline
client_b_seed >> client_b_run >> client_b_test

# Quality check after both clients complete
[client_a_test, client_b_test] >> quality_check

# Final steps
quality_check >> completion_report >> end
