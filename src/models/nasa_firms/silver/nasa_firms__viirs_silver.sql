{{
    config(
        materialized='incremental',
        unique_key='id',
        incremental_strategy='delete+insert'
    )
}}

WITH snpp AS (
    SELECT *
    FROM {{ ref('nasa_firms__viirs_snpp_stg') }}
    {% if is_incremental() %}
    WHERE
        acq_date = '{{ var('date') }}'::DATE
        AND country_id = '{{ var('country') }}'
    {% endif %}
),

noaa20 AS (
    SELECT *
    FROM {{ ref('nasa_firms__viirs_noaa20_stg') }}
    {% if is_incremental() %}
    WHERE
        acq_date = '{{ var('date') }}'::DATE
        AND country_id = '{{ var('country') }}'
    {% endif %}
),

noaa21 AS (
    SELECT *
    FROM {{ ref('nasa_firms__viirs_noaa21_stg') }}
    {% if is_incremental() %}
    WHERE
        acq_date = '{{ var('date') }}'::DATE
        AND country_id = '{{ var('country') }}'
    {% endif %}
),

unified AS (
    SELECT * FROM snpp
    UNION BY NAME
    SELECT * FROM noaa20
    UNION BY NAME
    SELECT * FROM noaa21
),

added_geometry AS (
    SELECT
        id,
        country_id,
        (acq_date::TEXT || ' ' || acq_time::TEXT)::TIMESTAMP AS timestamp,
        bright_ti4,
        bright_ti5,
        scan,
        track,
        satellite,
        instrument,
        confidence,
        version,
        frp,
        daynight,
        ST_POINT(latitude, longitude) AS geometry
    FROM unified
)

SELECT *
FROM added_geometry
