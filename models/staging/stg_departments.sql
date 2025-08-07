-- Staging model for department data
-- This model performs basic transformations and data type casting

{{ config(materialized='view') }}

select
    department_id,
    {{ apply_client_specific_transformations('name') }} as department_name,
    total_employees,
    description,
    -- Add audit columns using our macro
    {{ add_audit_columns(get_client_from_target()) }}
from {{ ref('department') }}
