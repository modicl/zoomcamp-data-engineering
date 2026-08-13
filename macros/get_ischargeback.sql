{% macro get_is_chargeback(total_amount) %}
case
    when {{ total_amount }} < 0 then 0
    when {{ total_amount }} > 1 then 1
    else 0
end
{%- endmacro %}
