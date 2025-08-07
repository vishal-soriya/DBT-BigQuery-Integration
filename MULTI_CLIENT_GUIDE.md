# Multi-Client DBT Configuration Guide

## Overview

This DBT project is configured for multi-tenancy, allowing you to run the same transformations for different clients with separate datasets. Currently configured for:

- **Client A**: Uses dataset `DBT_VISHAL_DATASET`
- **Client B**: Uses dataset `DBT_client_b_DATASET`

## Configuration Structure

### 1. Profiles Configuration (`profiles.yml`)

The profiles are configured with separate targets for each client and environment:

```yaml
bq_dbt_project:
  target: client_a_dev  # Default target
  outputs:
    # Client A
    client_a_dev: { dataset: DBT_VISHAL_DATASET }
    client_a_prod: { dataset: DBT_VISHAL_DATASET_PROD }
    
    # Client B  
    client_b_dev: { dataset: DBT_client_b_DATASET }
    client_b_prod: { dataset: DBT_client_b_DATASET_PROD }
```

### 2. Project Variables (`dbt_project.yml`)

Client-specific variables are configured to allow dynamic behavior:

```yaml
vars:
  client_id: "{{ env_var('DBT_CLIENT_ID', 'client_a') }}"
  client_a:
    table_prefix: "client_a_"
  client_b:
    table_prefix: "client_b_"
```

## Usage Methods

### Method 1: Using the Multi-Client Script (Recommended)

The `run_dbt_client.sh` script provides the easiest way to run DBT commands for specific clients:

```bash
# Basic syntax
./run_dbt_client.sh <client> <environment> <command> [additional_args]

# Examples
./run_dbt_client.sh client_a dev run
./run_dbt_client.sh client_b prod test
./run_dbt_client.sh client_a dev seed
./run_dbt_client.sh client_b dev build --select employee_details
./run_dbt_client.sh client_a dev docs
```

### Method 2: Direct DBT Commands

You can also run DBT commands directly by specifying the target:

```bash
# For Client A Development
dbt run --target client_a_dev
dbt test --target client_a_dev
dbt seed --target client_a_dev

# For Client B Production
dbt run --target client_b_prod
dbt test --target client_b_prod
```

## Common Workflows

### Initial Setup for Each Client

1. **Create BigQuery Datasets**:
   ```bash
   # Create datasets in BigQuery for each client
   # Client A: DBT_VISHAL_DATASET, DBT_VISHAL_DATASET_PROD
   # Client B: DBT_client_b_DATASET, DBT_client_b_DATASET_PROD
   ```

2. **Test Connections**:
   ```bash
   ./run_dbt_client.sh client_a dev debug
   ./run_dbt_client.sh client_b dev debug
   ```

3. **Load Seed Data**:
   ```bash
   ./run_dbt_client.sh client_a dev seed
   ./run_dbt_client.sh client_b dev seed
   ```

### Daily Operations

1. **Run transformations for Client A**:
   ```bash
   ./run_dbt_client.sh client_a dev build
   ```

2. **Run transformations for Client B**:
   ```bash
   ./run_dbt_client.sh client_b dev build
   ```

3. **Deploy to production**:
   ```bash
   ./run_dbt_client.sh client_a prod run
   ./run_dbt_client.sh client_b prod run
   ```

### Data Pipeline Integration

For automated data pipelines, you can use the scripts in your orchestration tools:

```bash
# In Apache Airflow, Prefect, or similar tools
bash_command="./run_dbt_client.sh client_a prod build"
```

## Environment Variables

You can use environment variables for additional flexibility:

```bash
# Set client ID
export DBT_CLIENT_ID=client_b

# Then run standard dbt commands (will use client_b configuration)
dbt run --target client_b_dev
```

## Adding New Clients

To add a new client (e.g., Client C):

1. **Update `profiles.yml`**:
   ```yaml
   client_c_dev:
     dataset: DBT_client_c_DATASET
     # ... other config
   ```

2. **Update `dbt_project.yml`**:
   ```yaml
   vars:
     client_c:
       table_prefix: "client_c_"
   ```

3. **Update scripts**:
   - Modify `run_dbt_client.sh` to accept `client_c`

## Troubleshooting

### Common Issues

1. **Dataset not found**:
   - Ensure the dataset exists in BigQuery
   - Check the target configuration in `profiles.yml`

2. **Permission errors**:
   - Verify service account has access to all client datasets
   - Check that the keyfile path is correct

3. **Wrong client data**:
   - Verify you're using the correct target
   - Check the `DBT_CLIENT_ID` environment variable

### Verification Commands

```bash
# Check which target is being used
dbt debug --target client_a_dev

# List all available targets
cat profiles.yml | grep -E "^\s+[a-z_]+:" | tr -d ':' | xargs

# Verify compiled SQL
dbt compile --target client_a_dev
```

## Best Practices

1. **Environment Isolation**: Always use separate prod datasets for each client
2. **Testing**: Run tests for each client after deployments
3. **Documentation**: Generate docs for each client separately if needed
4. **Monitoring**: Monitor data quality and pipeline success per client
5. **Naming Conventions**: Use consistent prefixes/suffixes for client-specific objects

## Security Considerations

1. **Service Account**: Consider using separate service accounts per client for better isolation
2. **Access Control**: Implement proper IAM roles for each client's datasets  
3. **Data Isolation**: Ensure no cross-client data access in models
4. **Audit Logging**: Monitor BigQuery audit logs for data access patterns

## Advanced Configuration

### Using Variables in Models

You can reference client configuration in your models:

```sql
-- models/staging/stg_employees.sql
{{ config(
    alias=var('client_id') + '_employees'
) }}

select
    employee_id,
    '{{ var("client_id") }}' as client_id,
    name as employee_name,
    -- ... rest of columns
from {{ ref('employee') }}
```

### Conditional Logic Based on Client

```sql
-- Different logic per client
select
    employee_id,
    {% if var('client_id') == 'client_a' %}
        upper(name) as employee_name  -- Client A wants uppercase names
    {% else %}
        name as employee_name  -- Client B wants normal case
    {% endif %}
from {{ ref('employee') }}
```

This setup provides a flexible, scalable multi-tenant DBT configuration that can grow with your client base!
