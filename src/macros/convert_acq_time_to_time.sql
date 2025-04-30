{% macro acq_time_to_time(column_name) %}

strftime(
    (current_date::TEXT
        || ' '
        || (FLOOR({{ column_name }}::INT / 100)::INT)::TEXT
        || ':'
        || LPAD(
            ({{ column_name }}::INT % 100)::TEXT,
            2,
            '0'
    ))::TIMESTAMP,
    '%I:%M'
)::TIME

{% endmacro %}
