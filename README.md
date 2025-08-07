# DBT-BigQuery-Integration

This is an open-source formatted DBT project that connects with Google BigQuery using service account authentication and runs transformation commands on sample employee and department data.

## 🚀 Multi-Client Support

This project is configured for **multi-tenancy**, allowing you to run the same transformations for different clients with separate BigQuery datasets:

- **Client A**: `DBT_VISHAL_DATASET`
- **Client B**: `DBT_client_b_DATASET`

**Quick Start for Multi-Client:**
```bash
# Run for Client A
./run_dbt_client.sh client_a dev run

# Run for Client B  
./run_dbt_client.sh client_b dev build

# Test connections
./run_dbt_client.sh client_a dev debug
./run_dbt_client.sh client_b dev debug

# Load seed data
./run_dbt_client.sh client_a dev seed
./run_dbt_client.sh client_b dev seed

# Run specific models
./run_dbt_client.sh client_a dev run --select employee_details
```

📖 **[Complete Multi-Client Guide](MULTI_CLIENT_GUIDE.md)**

## Project Structure

```
BQ-DBT/
├── dbt_project.yml              # DBT project configuration
├── profiles.yml                 # Database connection profiles  
├── requirements.txt             # Python dependencies
├── run_dbt_client.sh           # Multi-client runner script
├── run_dbt_client.ps1          # PowerShell version for Windows
├── MULTI_CLIENT_GUIDE.md       # Complete multi-client documentation
├── seeds/                       # CSV files for seeding data
│   ├── employee.csv             # Sample employee data
│   └── department.csv           # Sample department data
├── models/                      # DBT models
│   ├── staging/                 # Staging models (views)
│   │   ├── stg_employees.sql
│   │   ├── stg_departments.sql
│   │   └── schema.yml
│   └── marts/                   # Business-ready models (tables)
│       ├── employee_details.sql
│       └── schema.yml
├── macros/                      # Reusable DBT macros
├── tests/                       # Custom tests
├── analyses/                    # Analytical queries
└── snapshots/                   # DBT snapshots
```

## Prerequisites

1. **Google Cloud Platform Account**: You need a GCP account with BigQuery enabled
2. **Service Account**: Create a service account with BigQuery permissions
3. **Python 3.7+**: Ensure Python is installed on your system

## Setup Instructions

### 1. Google Cloud Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the BigQuery API
4. Create a service account:
   - Go to IAM & Admin > Service Accounts
   - Click "Create Service Account"
   - Give it a name like "dbt-bigquery-service-account"
   - Grant the following roles:
     - BigQuery Admin (or BigQuery Data Editor + BigQuery Job User)
     - BigQuery Data Viewer
5. Create and download the JSON key file
6. Rename the key file to `service-account-key.json` and place it in the project root

### 2. BigQuery Dataset Setup

1. Go to BigQuery in the Google Cloud Console
2. Create datasets:
   - `dbt_dev` (for development)
   - `dbt_prod` (for production)

### 3. Project Configuration

1. Update `profiles.yml`:
   - Replace `your-gcp-project-id` with your actual GCP project ID
   - Update dataset names if different
   - Ensure the keyfile path points to your service account key

### 4. Python Environment Setup

```bash
# Create a virtual environment
python -m venv dbt-env

# Activate the virtual environment
source dbt-env/bin/activate  # On macOS/Linux
# or
dbt-env\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 5. DBT Setup and Testing

```bash
# Test the connection
dbt debug

# Install any additional packages (if using packages.yml)
dbt deps

# Load seed data into BigQuery
dbt seed

# Run the models
dbt run

# Run tests
dbt test

# Generate and serve documentation
dbt docs generate
dbt docs serve
```

## Sample Data

### Employee Data (`seeds/employee.csv`)
- **employee_id**: Unique identifier for each employee
- **name**: Employee full name
- **location**: Employee work location
- **designation**: Job title
- **department_id**: Foreign key to department

### Department Data (`seeds/department.csv`)
- **department_id**: Unique identifier for each department
- **name**: Department name
- **total_employees**: Number of employees in the department
- **description**: Department description

## Models

### Staging Models (`models/staging/`)
- **stg_employees.sql**: Basic transformations on employee data
- **stg_departments.sql**: Basic transformations on department data

### Mart Models (`models/marts/`)
- **employee_details.sql**: Joined view of employees with department information

## Common DBT Commands

```bash
# Run all models
dbt run

# Run specific model
dbt run --select employee_details

# Run models and tests
dbt build

# Run only changed models and their downstream dependencies
dbt run --select state:modified+

# Compile models without running
dbt compile

# Generate documentation
dbt docs generate
dbt docs serve
```

## Environment Variables (Optional)

You can also use environment variables instead of hardcoding values in profiles.yml:

```bash
export DBT_PROJECT_ID=your-gcp-project-id
export DBT_DATASET=dbt_dev
export GOOGLE_APPLICATION_CREDENTIALS=./service-account-key.json
```

Then update your profiles.yml to use:
```yaml
project: "{{ env_var('DBT_PROJECT_ID') }}"
dataset: "{{ env_var('DBT_DATASET') }}"
keyfile: "{{ env_var('GOOGLE_APPLICATION_CREDENTIALS') }}"
```

## Troubleshooting

1. **Authentication Issues**: Ensure your service account key is valid and has the necessary permissions
2. **Dataset Not Found**: Make sure the datasets exist in BigQuery and match the names in profiles.yml
3. **Connection Timeout**: Increase the timeout_seconds value in profiles.yml
4. **Permission Denied**: Check that your service account has the required BigQuery roles

## Next Steps

1. Add more complex transformations in the models
2. Create custom macros for reusable logic
3. Implement data quality tests
4. Set up CI/CD pipelines
5. Add more sophisticated business logic models

## Resources

- [DBT Documentation](https://docs.getdbt.com/)
- [DBT BigQuery Adapter](https://docs.getdbt.com/reference/warehouse-setups/bigquery-setup)
- [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
