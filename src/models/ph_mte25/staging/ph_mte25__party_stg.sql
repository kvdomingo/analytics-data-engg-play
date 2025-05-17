{{
    config(
        materialized='incremental',
        unique_key='id',
        incremental_strategy='delete+insert'
    )
}}

SELECT
    {{ dbt_utils.generate_surrogate_key(['batch', 'region', 'name']) }} AS id,
    *
FROM {{ source('ae_de_play', 'ph_mte25__party_raw') }}
{% if is_incremental() %}
WHERE
    region = '{{ var('region') }}'
    AND batch = '{{ var('batch') }}'
{% endif %}
