{% test standard_date_format(model, column_name) %}

SELECT *
FROM {{ model }}
WHERE try_strptime({{ column_name }}::TEXT, '%Y-%m-%d') IS NULL

{% endtest %}
