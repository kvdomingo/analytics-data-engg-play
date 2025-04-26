{{
    config(
        materialized='incremental',
        unique_key='id',
        incremental_strategy='merge'
    )
}}

SELECT
    *,
    {{ dbt_utils.generate_surrogate_key(['acq_date', 'acq_time']) }} AS id
FROM {{ source('ae_de_play', 'nasa_firms__viirs_noaa20_raw') }}
{% if is_incremental() %}
WHERE date >= '{{ var('min_date') }}'::DATE
    AND date <= '{{ var('max_date') }}'
    AND country_id = '{{ var('country') }}'
{% endif %}
