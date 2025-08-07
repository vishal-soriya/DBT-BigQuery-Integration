-- Staging model for employee data
-- This model performs basic transformations and data type casting

{{ config(materialized='view') }}

select
    employee_id,
    name as employee_name,
    location,
    designation,
    department_id,
    current_timestamp() as _loaded_at
from {{ ref('employee') }}
