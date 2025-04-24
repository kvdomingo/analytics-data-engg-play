{% test adm_pcode_format(model, column_name) %}

SELECT *
FROM {{ model }}
WHERE NOT regexp_matches({{ column_name }}, '^PH\d{9}$')

{% endtest %}
