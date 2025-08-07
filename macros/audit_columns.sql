{% macro add_audit_columns(client_name='unknown') %}
    {#- This macro adds standard audit columns to any model -#}
    
    current_timestamp() as _dbt_loaded_at,
    '{{ client_name }}' as _client_name,
    '{{ target.name }}' as _environment,
    '{{ var("dbt_version", "1.0.0") }}' as _dbt_version

{% endmacro %}
