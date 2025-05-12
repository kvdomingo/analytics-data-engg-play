SELECT
    * EXCLUDE (uuid, freq),
    uuid AS id,
    freq AS frequency
FROM {{ ref('cchain__disease_pidsr_totals_stg') }}
