SELECT
    uuid AS id,
    date,
    adm3_pcode,
    adm4_pcode,
    disease_icd10_code,
    disease_common_name,
    sex,
    age_group,
    case_total,
    death_total
FROM {{ ref('cchain__disease_lgu_disaggregated_totals_stg') }}
