{{
    config(
        materialized='incremental',
        unique_key='id',
        incremental_strategy='merge'
    )
}}

WITH snpp AS (
    SELECT *
    FROM {{ ref('nasa_firms__viirs_snpp_bronze') }}
    {% if is_incremental() %}
    WHERE
        date = '{{ var('date') }}'::DATE
        AND country_id = '{{ var('country') }}'
    {% endif %}
),

noaa20 AS (
    SELECT *
    FROM {{ ref('nasa_firms__viirs_noaa20_bronze') }}
    {% if is_incremental() %}
    WHERE
        date = '{{ var('date') }}'::DATE
        AND country_id = '{{ var('country') }}'
    {% endif %}
),

noaa21 AS (
    SELECT *
    FROM {{ ref('nasa_firms__viirs_noaa21_bronze') }}
    {% if is_incremental() %}
    WHERE
        date = '{{ var('date') }}'::DATE
        AND country_id = '{{ var('country') }}'
    {% endif %}
)

SELECT * FROM snpp
UNION ALL BY NAME
SELECT * FROM noaa20
UNION ALL BY NAME
SELECT * FROM noaa21
