{% macro get_client_from_target() %}
    {#- Extract client name from target name (e.g., client_a_dev -> client_a) -#}
    
    {% set target_parts = target.name.split('_') %}
    {% if target_parts | length >= 2 %}
        {% set client_name = target_parts[0] + '_' + target_parts[1] %}
    {% else %}
        {% set client_name = 'default' %}
    {% endif %}
    
    {{ return(client_name) }}

{% endmacro %}


{% macro apply_client_specific_transformations(column_name) %}
    {#- Apply different transformations based on client -#}
    
    {% set client = get_client_from_target() %}
    
    {% if client == 'client_a' %}
        {#- Client A wants all names in uppercase -#}
        upper({{ column_name }}) as {{ column_name }}
    {% elif client == 'client_b' %}
        {#- Client B wants proper case (title case) -#}
        initcap({{ column_name }}) as {{ column_name }}
    {% else %}
        {#- Default: no transformation -#}
        {{ column_name }}
    {% endif %}

{% endmacro %}
