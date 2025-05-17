{{
    config(
        materialized='incremental',
        unique_key='id',
        incremental_strategy='delete+insert'
    )
}}

SELECT *
FROM {{ ref('ph_mte25__party_stg') }}
