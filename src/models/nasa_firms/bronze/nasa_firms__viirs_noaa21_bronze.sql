{{
    config(
        materialized='incremental',
        unique_key='id',
        incremental_strategy='merge'
    )
}}

SELECT
    {{ dbt_utils.generate_surrogate_key(['acq_date', 'acq_time']) }} AS id,
    country_id,
    latitude::FLOAT AS latitude,
    longitude::FLOAT AS longitude,
    bright_ti4::FLOAT AS bright_ti4,
    bright_ti5::FLOAT AS bright_ti5,
    scan::FLOAT AS scan,
    track::FLOAT AS track,
    acq_date::DATE AS acq_date
    {{ acq_time_to_time('acq_time') }}::TIME AS acq_time,
    satellite,
    instrument,
    confidence,
    version,
    frp::FLOAT AS frp,
    daynight
FROM {{ source('ae_de_play', 'nasa_firms__viirs_noaa21_raw') }}
{% if is_incremental() %}
WHERE
    acq_date = '{{ var('date') }}'::DATE
    AND country_id = '{{ var('country') }}'
{% endif %}
