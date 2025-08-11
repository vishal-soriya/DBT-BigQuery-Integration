# Airflow Setup for DBT Multi-Client Transformations

This directory contains Apache Airflow configuration to orchestrate DBT transformations for multiple clients using Docker Compose.

## 📁 Directory Structure

```
airflow/
├── docker-compose.yml          # Airflow services configuration
├── airflow.sh                  # Management script
├── .env                        # Environment variables
├── dags/                       # Airflow DAGs
│   ├── dbt_multi_client_dag.py           # Sequential client processing
│   ├── dbt_multi_client_parallel.py     # Parallel client processing
│   └── dbt_production_deployment.py     # Production deployment
├── logs/                       # Airflow logs
├── plugins/                    # Custom Airflow plugins
└── config/                     # Airflow configuration
```

## 🚀 Quick Start

### 1. **Prerequisites**
- Docker and Docker Compose installed
- At least 4GB RAM available for Docker

### 2. **Initial Setup**
```bash
cd airflow
./airflow.sh init
```

### 3. **Start Airflow**
```bash
./airflow.sh start
```

### 4. **Access Web UI**
- URL: http://localhost:8080
- Username: `airflow`
- Password: `airflow`

## 📋 Available DAGs

### 1. **dbt_multi_client_transformations** 
- **Schedule**: Daily at 2 AM
- **Description**: Sequential processing of Client A → Client B
- **Pipeline**: seed → run → test for each client

### 2. **dbt_multi_client_parallel**
- **Schedule**: Daily at 6 AM  
- **Description**: Parallel processing of both clients
- **Pipeline**: Both clients run simultaneously

### 3. **dbt_production_deployment**
- **Schedule**: Manual trigger only
- **Description**: Production deployment with quality checks
- **Pipeline**: Production run → tests → documentation

## 🛠️ Management Commands

```bash
# Initialize Airflow (first time only)
./airflow.sh init

# Start all services
./airflow.sh start

# Stop all services
./airflow.sh stop

# Restart services
./airflow.sh restart

# View logs
./airflow.sh logs

# Check status
./airflow.sh status

# Clean up (removes all data!)
./airflow.sh cleanup
```

## 🎯 DAG Details

### Sequential DAG Flow
```
Start → Client A Seed → Client A Run → Client A Test
         ↓
      Client B Seed → Client B Run → Client B Test → End
```

### Parallel DAG Flow
```
Start → [Client A Seed, Client B Seed]
         ↓                    ↓
      Client A Run        Client B Run
         ↓                    ↓
      Client A Test       Client B Test
         ↓                    ↓
                End
```

## 🔧 Configuration

### Environment Variables (.env)
```bash
AIRFLOW_UID=50000                    # Airflow user ID
AIRFLOW_PROJ_DIR=.                   # Airflow project directory
DBT_PROJ_DIR=../                     # DBT project directory (relative to airflow/)
_AIRFLOW_WWW_USER_USERNAME=airflow   # Web UI username
_AIRFLOW_WWW_USER_PASSWORD=airflow   # Web UI password
```

### Docker Compose Services
- **airflow-webserver**: Web UI (port 8080)
- **airflow-scheduler**: Task scheduler
- **postgres**: Metadata database
- **airflow-init**: One-time initialization

## 📊 Monitoring

### Web UI Features
- **DAGs**: View and manage all workflows
- **Task Instances**: Monitor individual task execution
- **Logs**: View detailed task logs
- **Graph View**: Visualize DAG dependencies
- **Gantt Chart**: Timeline view of task execution

### Task Status
- 🟢 **Success**: Task completed successfully
- 🔴 **Failed**: Task failed and needs attention
- 🟡 **Running**: Task currently executing
- ⚪ **Queued**: Task waiting to run
- 🔵 **Skipped**: Task was skipped

## 🚨 Troubleshooting

### Common Issues

1. **Port 8080 already in use**
   ```bash
   # Change port in docker-compose.yml
   ports:
     - "8081:8080"  # Use port 8081 instead
   ```

2. **Permission denied errors**
   ```bash
   # On Linux, set proper UID
   echo -e "AIRFLOW_UID=$(id -u)" > .env
   ```

3. **DBT command not found**
   - Verify DBT is installed in the Docker container
   - Check the volume mount paths in docker-compose.yml

4. **Service account key not found**
   - Ensure `dbt-bq-service-key.json` is in the project root
   - Check file permissions

### Viewing Logs
```bash
# View all logs
./airflow.sh logs

# View specific service logs
docker-compose logs airflow-webserver
docker-compose logs airflow-scheduler

# View task logs in Web UI
# Navigate to DAGs → Select DAG → Task Instances → Click on task → View Logs
```

### Debugging DAGs
```bash
# Test DAG parsing
docker-compose exec airflow-webserver airflow dags list

# Test specific DAG
docker-compose exec airflow-webserver airflow dags test dbt_multi_client_transformations 2025-08-11
```

## 🔒 Security

### Default Credentials
- **Username**: airflow  
- **Password**: airflow
- **⚠️ Change these for production use!**

### Service Account
- The BigQuery service account key is mounted from the parent directory
- Ensure proper IAM permissions for all client datasets

## 📈 Performance

### Resource Requirements
- **Memory**: Minimum 4GB RAM
- **CPU**: 2+ cores recommended
- **Storage**: 10GB+ available disk space

### Scaling
- Increase `parallelism` in airflow.cfg for more concurrent tasks
- Use `CeleryExecutor` for distributed processing
- Add worker nodes for larger workloads

## 🔄 Backup & Recovery

### Database Backup
```bash
# Backup Postgres metadata
docker-compose exec postgres pg_dump -U airflow airflow > airflow_backup.sql
```

### Configuration Backup
- Back up the entire `airflow/` directory
- Include `.env` file with sensitive configurations
- Store service account keys securely

## 🎉 Next Steps

1. **Custom DAGs**: Create client-specific DAGs in the `dags/` folder
2. **Notifications**: Add email/Slack notifications to DAGs
3. **Data Quality**: Implement custom data quality checks
4. **Monitoring**: Set up external monitoring with Prometheus/Grafana
5. **CI/CD**: Integrate DAG deployment with your CI/CD pipeline

## 📚 Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [DBT Documentation](https://docs.getdbt.com/)
- [Docker Compose Guide](https://docs.docker.com/compose/)
- [BigQuery Integration](https://cloud.google.com/bigquery/docs)

Happy orchestrating! 🎼
