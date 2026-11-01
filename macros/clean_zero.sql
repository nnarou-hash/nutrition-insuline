{% macro clean_zero(column) %}
    case when abs({{ column }}) < 1e-70 then 0 else {{ column }} end
{% endmacro %}
