-- Staging model for employee data
-- This model performs basic transformations and data type casting

{{ config(materialized='view') }}

select
    employee_id,
    {{ apply_client_specific_transformations('name') }} as employee_name,
    location,
    designation,
    department_id,
    -- Add audit columns using our macro
    {{ add_audit_columns(get_client_from_target()) }}
from {{ ref('employee') }}
