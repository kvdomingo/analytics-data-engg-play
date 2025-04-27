{% macro acq_time_to_time(column_name) %}

strftime(
    (current_date::TEXT
        || ' '
        || (FLOOR({{ column_name }} / 100)::INT)::TEXT
        || ':'
        || LPAD(
            ({{ column_name }} - FLOOR({{ column_name }} / 100)::INT * 100)::TEXT,
            2,
            '0'
    ))::TIMESTAMP,
    '%I:%M'
)

{% endmacro %}
