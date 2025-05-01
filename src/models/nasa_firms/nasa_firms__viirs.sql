{{
    config(
        materialized='incremental',
        unique_key='id',
        incremental_strategy='delete+insert'
    )
}}

SELECT *
FROM {{ ref('nasa_firms__viirs_silver') }}
{% if is_incremental() %}
WHERE date = '{{ var('date') }}'::DATE
    AND country_id = '{{ var('country') }}'
{% endif %}
