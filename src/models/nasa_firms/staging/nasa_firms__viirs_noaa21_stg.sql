{{
    config(
        materialized='incremental',
        unique_key='id',
        incremental_strategy='delete+insert'
    )
}}

SELECT *
FROM {{ ref('nasa_firms__viirs_noaa21_bronze') }}
{% if is_incremental() %}
WHERE
    acq_date = '{{ var('date') }}'::DATE
    AND country_id = '{{ var('country') }}'
{% endif %}
