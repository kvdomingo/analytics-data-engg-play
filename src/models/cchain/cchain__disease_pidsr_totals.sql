SELECT
    uuid AS id,
    freq AS frequency,
    date,
    adm3_pcode,
    disease_icd10_code,
    disease_common_name,
    case_total
FROM {{ ref('cchain__disease_pidsr_totals_stg') }}
