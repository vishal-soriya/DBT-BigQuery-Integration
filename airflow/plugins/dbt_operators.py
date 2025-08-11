"""
Custom DBT Operator for Airflow

This operator provides enhanced DBT functionality including:
- Better error handling
- Progress tracking
- Custom logging
- Integration with Airflow XComs

Author: Auto-generated
"""

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException
import subprocess
import logging
import json
import os
from datetime import datetime


class DBTClientOperator(BaseOperator):
    """
    Custom operator to run DBT commands for specific clients
    
    :param client: Client name (client_a, client_b)
    :param environment: Environment (dev, prod)
    :param dbt_command: DBT command to run (run, test, seed, etc.)
    :param dbt_project_dir: Path to DBT project directory
    :param select: Optional select statement for models
    :param exclude: Optional exclude statement for models
    :param full_refresh: Whether to perform full refresh
    """
    
    template_fields = ['client', 'environment', 'dbt_command', 'select']
    
    @apply_defaults
    def __init__(
        self,
        client: str,
        environment: str,
        dbt_command: str,
        dbt_project_dir: str = '/opt/airflow/dbt_project',
        select: str = None,
        exclude: str = None,
        full_refresh: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.client = client
        self.environment = environment
        self.dbt_command = dbt_command
        self.dbt_project_dir = dbt_project_dir
        self.select = select
        self.exclude = exclude
        self.full_refresh = full_refresh
        
    def execute(self, context):
        """Execute the DBT command"""
        
        # Build the command
        cmd = self._build_command()
        
        # Log the command being executed
        self.log.info(f"Executing DBT command: {' '.join(cmd)}")
        
        # Change to project directory
        original_dir = os.getcwd()
        
        try:
            os.chdir(self.dbt_project_dir)
            
            # Execute the command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour timeout
            )
            
            # Log output
            if result.stdout:
                self.log.info(f"DBT Output:\n{result.stdout}")
                
            if result.stderr:
                self.log.warning(f"DBT Warnings/Errors:\n{result.stderr}")
            
            # Check for success
            if result.returncode != 0:
                error_msg = f"DBT command failed with return code {result.returncode}"
                if result.stderr:
                    error_msg += f"\nError: {result.stderr}"
                raise AirflowException(error_msg)
            
            # Parse and return results
            results = self._parse_results(result.stdout)
            
            # Push results to XCom for downstream tasks
            context['task_instance'].xcom_push(
                key='dbt_results',
                value=results
            )
            
            self.log.info(f"✅ DBT command completed successfully for {self.client}_{self.environment}")
            return results
            
        except subprocess.TimeoutExpired:
            error_msg = f"DBT command timed out after 1 hour"
            self.log.error(error_msg)
            raise AirflowException(error_msg)
            
        except Exception as e:
            error_msg = f"Error executing DBT command: {str(e)}"
            self.log.error(error_msg)
            raise AirflowException(error_msg)
            
        finally:
            # Return to original directory
            os.chdir(original_dir)
    
    def _build_command(self):
        """Build the DBT command with all arguments"""
        
        cmd = ['./run_dbt_client.sh', self.client, self.environment, self.dbt_command]
        
        if self.select:
            cmd.extend(['--select', self.select])
            
        if self.exclude:
            cmd.extend(['--exclude', self.exclude])
            
        if self.full_refresh and self.dbt_command == 'run':
            cmd.append('--full-refresh')
            
        return cmd
    
    def _parse_results(self, output: str) -> dict:
        """Parse DBT output for key metrics"""
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'client': self.client,
            'environment': self.environment,
            'command': self.dbt_command,
            'status': 'success'
        }
        
        # Extract key metrics from output
        lines = output.split('\n')
        
        for line in lines:
            if 'Done.' in line and ('PASS=' in line or 'ERROR=' in line):
                # Parse final summary line
                # Example: "Done. PASS=3 WARN=0 ERROR=0 SKIP=0 TOTAL=3"
                parts = line.split()
                for part in parts:
                    if '=' in part:
                        key, value = part.split('=')
                        try:
                            results[key.lower()] = int(value)
                        except ValueError:
                            results[key.lower()] = value
                            
            elif 'Completed successfully' in line:
                results['status'] = 'success'
                
            elif 'Completed with' in line and 'error' in line:
                results['status'] = 'completed_with_errors'
        
        return results


class DBTTestOperator(DBTClientOperator):
    """Specialized operator for DBT tests"""
    
    @apply_defaults
    def __init__(self, **kwargs):
        kwargs['dbt_command'] = 'test'
        super().__init__(**kwargs)


class DBTRunOperator(DBTClientOperator):
    """Specialized operator for DBT run"""
    
    @apply_defaults 
    def __init__(self, **kwargs):
        kwargs['dbt_command'] = 'run'
        super().__init__(**kwargs)


class DBTSeedOperator(DBTClientOperator):
    """Specialized operator for DBT seed"""
    
    @apply_defaults
    def __init__(self, **kwargs):
        kwargs['dbt_command'] = 'seed'
        super().__init__(**kwargs)
