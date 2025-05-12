SELECT
    * EXCLUDE (uuid),
    uuid AS id
FROM {{ ref('cchain__disease_lgu_disaggregated_totals_stg') }}
