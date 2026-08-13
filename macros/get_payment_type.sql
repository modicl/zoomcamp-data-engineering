{% macro get_payment_type_name(payment_type) %}
case
    when {{ payment_type }} = 1 then 'Creative Mobile Technologies, LLC'
    when {{ payment_type }} = 2 then 'VeriFone Inc.'
    when {{ payment_type }} = 4 then 'Unknown Vendor'
end
{%- endmacro %}
