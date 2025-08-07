{% macro get_client_table_name(base_name, client_suffix='') %}
    {#- 
    This macro generates client-specific table names
    Usage: {{ get_client_table_name('employees', 'client_a') }}
    Result: client_a_employees
    -#}
    
    {% if client_suffix %}
        {{ client_suffix }}_{{ base_name }}
    {% else %}
        {{ base_name }}
    {% endif %}

{% endmacro %}
