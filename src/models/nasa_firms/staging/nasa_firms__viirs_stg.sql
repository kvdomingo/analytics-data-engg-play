{{
    config(
        materialized='incremental',
        unique_key='id',
        incremental_strategy='merge'
    )
}}

SELECT *
FROM {{ ref('nasa_firms__viirs_snpp_bronze') }}
{% if is_incremental() %}
WHERE
    date >= '{{ var('min_date') }}'::DATE
    AND date <= '{{ var('max_date') }}'
    AND country_id = '{{ var('country') }}'
{% endif %}

UNION ALL BY NAME

SELECT *
FROM {{ ref('nasa_firms__viirs_noaa20_bronze') }}
{% if is_incremental() %}
WHERE
    date >= '{{ var('min_date') }}'::DATE
    AND date <= '{{ var('max_date') }}'
    AND country_id = '{{ var('country') }}'
{% endif %}

UNION ALL BY NAME

SELECT *
FROM {{ ref('nasa_firms__viirs_noaa21_bronze') }}
{% if is_incremental() %}
WHERE
    date >= '{{ var('min_date') }}'::DATE
    AND date <= '{{ var('max_date') }}'
    AND country_id = '{{ var('country') }}'
{% endif %}
