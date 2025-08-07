-- Staging model for department data
-- This model performs basic transformations and data type casting

{{ config(materialized='view') }}

select
    department_id,
    name as department_name,
    total_employees,
    description,
    current_timestamp() as _loaded_at
from {{ ref('department') }}
