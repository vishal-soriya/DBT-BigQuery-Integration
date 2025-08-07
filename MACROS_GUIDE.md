# DBT Macros Guide

## What are DBT Macros?

Macros are **reusable functions** written in Jinja templating language that generate SQL dynamically. They help you:

- 📝 Write DRY (Don't Repeat Yourself) code
- 🔧 Create reusable SQL snippets
- 🎯 Generate different SQL based on conditions
- 📊 Add consistent patterns across models

## Macro Examples in This Project

### 1. `add_audit_columns()` - Standard Audit Fields

**Purpose**: Adds consistent audit columns to all models.

```sql
{% macro add_audit_columns(client_name='unknown') %}
    current_timestamp() as _dbt_loaded_at,
    '{{ client_name }}' as _client_name,
    '{{ target.name }}' as _environment,
    '{{ var("dbt_version", "1.0.0") }}' as _dbt_version
{% endmacro %}
```

**Usage in Models**:
```sql
select
    employee_id,
    name,
    {{ add_audit_columns(get_client_from_target()) }}
from {{ ref('employee') }}
```

**Generated SQL for Client A**:
```sql
select
    employee_id,
    name,
    current_timestamp() as _dbt_loaded_at,
    'client_a' as _client_name,
    'client_a_dev' as _environment,
    '1.0.0' as _dbt_version
from `project.dataset.employee`
```

### 2. `apply_client_specific_transformations()` - Client-Specific Logic

**Purpose**: Apply different transformations based on the client.

```sql
{% macro apply_client_specific_transformations(column_name) %}
    {% set client = get_client_from_target() %}
    
    {% if client == 'client_a' %}
        upper({{ column_name }}) as {{ column_name }}
    {% elif client == 'client_b' %}
        initcap({{ column_name }}) as {{ column_name }}
    {% else %}
        {{ column_name }}
    {% endif %}
{% endmacro %}
```

**Results**:
- **Client A**: Names in UPPERCASE
- **Client B**: Names in Title Case
- **Others**: No transformation

### 3. `get_client_from_target()` - Extract Client Info

**Purpose**: Automatically determine client from target name.

```sql
{% macro get_client_from_target() %}
    {% set target_parts = target.name.split('_') %}
    {% if target_parts | length >= 2 %}
        {% set client_name = target_parts[0] + '_' + target_parts[1] %}
    {% else %}
        {% set client_name = 'default' %}
    {% endif %}
    {{ return(client_name) }}
{% endmacro %}
```

**Examples**:
- `client_a_dev` → `client_a`
- `client_b_prod` → `client_b`

## How to Use Macros

### 1. **Create Macro Files**
Place macro files in the `macros/` directory:
```
macros/
├── audit_columns.sql
├── client_utils.sql
└── client_transformations.sql
```

### 2. **Call Macros in Models**
Use `{{ macro_name(parameters) }}` syntax:
```sql
select
    id,
    {{ apply_client_specific_transformations('name') }},
    {{ add_audit_columns('my_client') }}
from {{ ref('source_table') }}
```

### 3. **Test with Compilation**
Use `dbt compile` to see generated SQL:
```bash
dbt compile --target client_a_dev --select model_name
```

## Advanced Macro Patterns

### 1. **Conditional Schema Creation**
```sql
{% macro generate_schema_name(custom_schema_name, node) -%}
    {% if custom_schema_name is none %}
        {{ target.schema }}
    {% else %}
        {{ target.schema }}_{{ custom_schema_name | trim }}
    {% endif %}
{%- endmacro %}
```

### 2. **Dynamic Column Generation**
```sql
{% macro get_column_list(table_name, exclude_columns=[]) %}
    {% set columns = adapter.get_columns_in_relation(ref(table_name)) %}
    {% set column_names = [] %}
    
    {% for column in columns %}
        {% if column.name not in exclude_columns %}
            {% do column_names.append(column.name) %}
        {% endif %}
    {% endfor %}
    
    {{ return(column_names | join(', ')) }}
{% endmacro %}
```

### 3. **Environment-Specific Logic**
```sql
{% macro get_warehouse_size() %}
    {% if target.name == 'prod' %}
        {{ return('LARGE') }}
    {% else %}
        {{ return('SMALL') }}
    {% endif %}
{% endmacro %}
```

## Best Practices

### 1. **Naming Conventions**
- Use descriptive names: `add_audit_columns()` not `audit()`
- Group related macros: `client_transformations.sql`

### 2. **Documentation**
- Add comments explaining macro purpose
- Document parameters and return values

### 3. **Error Handling**
```sql
{% macro safe_divide(numerator, denominator) %}
    case 
        when {{ denominator }} = 0 then null
        else {{ numerator }} / {{ denominator }}
    end
{% endmacro %}
```

### 4. **Testing Macros**
- Use `dbt compile` to verify generated SQL
- Test with different target environments
- Create sample models to validate macro behavior

## Common Use Cases

1. **Standardization**: Consistent date formatting, naming conventions
2. **Multi-tenancy**: Client-specific transformations
3. **Environment Logic**: Different behavior for dev/prod
4. **Code Reuse**: Complex calculations, window functions
5. **Dynamic SQL**: Conditional columns, table names

## Debugging Macros

### View Generated SQL:
```bash
# Compile to see final SQL
dbt compile --select model_name

# Check compiled files
cat target/compiled/project_name/models/model_name.sql
```

### Debug Macro Logic:
```sql
-- Add debug prints in macros
{% macro debug_macro() %}
    {{ log("Debug: target.name = " ~ target.name, info=true) }}
{% endmacro %}
```

## Performance Considerations

- Macros run during compilation, not execution
- Complex macros can slow down compilation
- Use macros for logic, not for large data transformations
- Consider materialized views for heavy computations

This macro system makes your DBT project more maintainable and allows for sophisticated multi-client logic! 🚀
