-- Employee details with department information
-- This is a business-ready model combining employee and department data

{{ config(materialized='view') }}

with employee_with_department as (
    select
        e.employee_id,
        e.employee_name,
        e.location,
        e.designation,
        e.department_id,
        d.department_name,
        d.description as department_description,
        d.total_employees as department_total_employees,
        e._loaded_at
    from {{ ref('stg_employees') }} e
    left join {{ ref('stg_departments') }} d
        on e.department_id = d.department_id
)

select * from employee_with_department
