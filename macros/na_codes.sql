{% macro na_codes(column) %}
    case when {{ column }} in (7777, 9999) then null else {{ column }} end
{% endmacro %}
